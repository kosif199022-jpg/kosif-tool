#!/usr/bin/env python3
"""Build data/mind_registry.json: ONE deduplicated registry of thinking frameworks.

Merges four sources that grew separately in this repo:
  dragon-mind     .claude/skills/kosif-dragon-mind/data/frameworks.json       (stage already set)
  thinking-books  .claude/skills/kosif-superpowers/data/thinking_books.json   (9 stages -> 6)
  book-methods    .claude/skills/kosif-superpowers/data/book_methods.json     (domain -> stage)
  mental-models   .claude/skills/kosif-superpowers/data/mental_models.json    (discipline -> stage)

Every entry is keyed by a normalized name, mapped onto the six Dragon Mind stages
(frame / explore / decide / build / verify / learn), lists every `sources[]` it came from,
and carries a `video` tag set (hook, story, rhythm, emotion, contrast, critique) with weights
so the montage brain can pick a few deep frameworks per step instead of all of them.

    python3 build_mind_registry.py            # writes ../data/mind_registry.json, prints counts
    python3 build_mind_registry.py --check    # rebuild in memory and compare with the file

Stdlib only, deterministic (sorted keys, no timestamps).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import dm_common as C  # noqa: E402

OUT = C.SKILL / "data" / "mind_registry.json"
STAGES = ["frame", "explore", "decide", "build", "verify", "learn"]
TAGS = ["hook", "story", "rhythm", "emotion", "contrast", "critique"]

SOURCES = {
    "dragon-mind": C.MIND / "data" / "frameworks.json",
    "thinking-books": C.SP_DATA / "thinking_books.json",
    "book-methods": C.SP_DATA / "book_methods.json",
    "mental-models": C.SP_DATA / "mental_models.json",
}

# thinking_books has nine stages; the Dragon Mind has six.
TB_STAGE = {"frame": "frame", "diverge": "explore", "converge": "decide", "forecast": "decide",
            "decide": "decide", "execute": "build", "verify": "verify", "communicate": "build",
            "learn": "learn"}
BM_DOMAIN = {"lateral": "explore", "conceptual": "explore", "engineering": "build", "accounting": "verify",
             "personality": "frame", "cinematography": "build", "bayesian": "decide", "prompting": "build",
             "arabic-verse": "build", "teaching": "learn", "logic": "verify", "drama": "build"}
MM_DISCIPLINE = {"decision": "decide", "prioritisation": "decide", "probability": "decide",
                 "forecasting": "decide", "economics": "decide", "strategy": "decide", "quantitative": "decide",
                 "planning": "build", "engineering": "build", "product": "build", "capability": "build",
                 "communication": "build", "systems": "frame", "structuring": "frame", "diagnosis": "frame",
                 "complexity": "frame", "reasoning": "frame", "people": "frame", "creativity": "explore",
                 "biases": "verify", "epistemics": "verify", "argument": "verify", "learning": "learn"}
# Name-level overrides where the source category puts a method in the wrong step.
STAGE_OVERRIDE = {"pre mortem": "verify", "red team": "verify", "kill criteria": "decide",
                  "debugging discipline": "verify", "estimate units ranges model": "decide",
                  "evaluation release gates saudi controls": "verify", "reviews then measure before tuning": "verify",
                  "steelman": "verify", "falsifiability": "verify", "calibration": "verify",
                  "inversion": "explore", "analogy transfer": "explore"}

STOP = {"the", "a", "an", "of", "and", "vs", "to", "for", "with", "check", "then", "your", "on", "is"}

# Variant normalized name -> canonical key. Canonical keys of dragon-mind entries are their
# slug ids with "-" turned to " "; the rest use their own normalized name.
ALIASES = {
    # mental models
    "second order effects": "second order thinking",
    "occams razor": "occams razor",
    "base rates": "outside view",
    "reversible irreversible one way doors": "one way two way doors",
    "pareto 80 20": "pareto principle",
    "mece": "issue tree mece",
    "issue tree": "issue tree mece",
    "lateral thinking provocation": "lateral thinking",
    "deliberate practice loop": "deliberate practice",
    "confirmation bias": "tfs confirmation",
    "anchoring": "tfs anchoring",
    "regret minimisation": "regret minimization",
    "weighted decision matrix": "pugh matrix",
    "minimum viable slice": "mvp",
    "divergent convergent": "double diamond",
    # thinking books
    "outside view first reference class": "outside view",
    "wysiati what you see all there": "tfs wysiati",
    "anchor availability sweep": "tfs anchoring",
    "mediating assessments protocol": "decision hygiene mediating assessments",
    "named bias checklist before sending": "cognitive bias checklist",
    "fermi ize question": "fermi estimation",
    "anti resulting review": "resulting decision quality",
    "ten ten ten ulysses contract": "ten ten ten",
    "fragility test via negativa": "via negativa",
    "contradiction inventive principles": "triz",
    "answer first pyramid scqa": "pyramid principle",
    "hypothesis driven 7 steps": "hypothesis driven problem solving",
    "hat sequence": "six thinking hats",
    "po provocation": "provocation po",
    "scamper sweep": "scamper",
    "stock flow loop map": "stocks and flows",
    "leverage point ladder": "leverage points",
    "system archetype match": "system archetypes",
    "wrap": "wrap process",
    "riskiest assumption test mvp": "mvp",
    "success message": "made to stick success",
    "pause point checklist": "checklist",
    "explore exploit budget": "explore exploit",
    "keep score brier style": "calibration",
    "calibrated 90 range value information": "calibration",
    "bias tests double standard outsider conformity status quo": "cognitive bias checklist",
    # book methods
    "two stages thinking idea processing": "double diamond",
    "provocation work forward from nonsense statement": "provocation po",
    "estimate units ranges model": "fermi estimation",
    "be absolutely clear about problem": "problem reframing",
    "dig requirements solve real puzzle": "problem reframing",
}


def norm(name: str) -> str:
    s = unicodedata.normalize("NFKC", name).lower().replace("'", "").replace("’", "")
    s = re.sub(r"[^a-z0-9]+", " ", s)
    words = [w for w in s.split() if w not in STOP]
    return " ".join(words)


# Hand-written keys are normalized the same way as the data, so a stop word never breaks a match.
ALIASES = {norm(k): norm(v) for k, v in ALIASES.items()}
STAGE_OVERRIDE = {norm(k): v for k, v in STAGE_OVERRIDE.items()}


# ---------------------------------------------------------------- video relevance

TAG_WORDS = {
    "hook": ["hook", "attention", "first", "surprise", "curiosity", "question", "opening", "provocation", "sticky",
             "stick", "unexpected", "frame", "anchor", "hooked", "خطاف", "هوك", "انتباه", "مفاجأة", "فضول", "سؤال"],
    "story": ["story", "narrative", "arc", "hero", "journey", "message", "sparkline", "pyramid", "scqa", "why",
              "persuasion", "character", "قصة", "حكاية", "سرد", "رسالة", "بطل", "قوس"],
    "rhythm": ["rhythm", "tempo", "pace", "beat", "timing", "flow", "sequence", "frame rate", "shutter", "loop",
               "queue", "seconds", "إيقاع", "ايقاع", "توقيت", "تتابع", "سرعة"],
    "emotion": ["emotion", "feeling", "affect", "peak", "ending", "remembered", "regret", "loss", "fear", "tone",
                "motivation", "identity", "redemption", "شعور", "عاطفة", "انفعال", "إحساس", "ذروة", "نهاية"],
    "contrast": ["contrast", "contradiction", "invert", "inversion", "opposite", "before", "versus", "paradox",
                 "reverse", "framing", "provocation", "reframe", "challenge", "تناقض", "عكس", "مقارنة", "قبل", "بعد"],
    "critique": ["review", "bias", "audit", "red team", "pre mortem", "failure", "risk", "check", "test", "doubt",
                 "falsif", "noise", "verify", "مراجعة", "نقد", "انحياز", "مخاطر", "فشل", "اختبار"],
}
# Hand-set weights for the frameworks that matter most to an editor (the keyword pass is only a floor).
MANUAL = {
    "made to stick success": {"hook": 0.95, "story": 0.7, "emotion": 0.6},
    "storybrand": {"story": 0.9, "hook": 0.5},
    "resonate sparkline": {"contrast": 0.95, "story": 0.85, "emotion": 0.6},
    "golden circle": {"story": 0.75, "hook": 0.6},
    "pyramid principle": {"hook": 0.6, "story": 0.6},
    "hook model": {"hook": 0.85, "rhythm": 0.4},
    "tfs two selves": {"emotion": 0.95, "story": 0.8, "rhythm": 0.7},
    "tfs framing": {"hook": 0.8, "contrast": 0.8},
    "tfs loss aversion": {"hook": 0.75, "emotion": 0.7},
    "tfs affect heuristic": {"emotion": 0.85},
    "tfs cognitive ease": {"rhythm": 0.6, "hook": 0.5},
    "tfs norms surprise causes": {"hook": 0.8, "contrast": 0.6},
    "tfs narrative fallacy": {"critique": 0.7, "story": 0.6},
    "tfs availability": {"hook": 0.5},
    "tfs priming": {"hook": 0.55, "rhythm": 0.4},
    "provocation po": {"hook": 0.7, "contrast": 0.85},
    "lateral thinking": {"contrast": 0.7, "hook": 0.5},
    "scamper": {"contrast": 0.75},
    "triz": {"contrast": 0.6},
    "inversion": {"contrast": 0.85, "critique": 0.6},
    "first principles": {"story": 0.5, "critique": 0.4},
    "problem reframing": {"hook": 0.6, "story": 0.5},
    "jobs to be done": {"story": 0.55},
    "theory mind reader model": {"hook": 0.75, "critique": 0.6},
    "six thinking hats": {"critique": 0.75, "emotion": 0.6},
    "pre mortem": {"critique": 0.95},
    "red team": {"critique": 0.9},
    "cognitive bias checklist": {"critique": 0.7},
    "double diamond": {"contrast": 0.4, "story": 0.3},
    "morphological analysis": {"contrast": 0.6},
    "medici intersection": {"contrast": 0.65},
    "synectics": {"contrast": 0.6},
    "pugh matrix": {"critique": 0.5},
    "timed emotional arc platform tone": {"emotion": 0.95, "rhythm": 0.9, "story": 0.8},
    "shutter motion blur frame rate": {"rhythm": 0.7},
    "look serves story inside budget": {"story": 0.75},
    "narrative identity redemption contamination": {"story": 0.85, "emotion": 0.8},
    "approach avoidance motivation rst": {"hook": 0.6, "emotion": 0.6},
    "flow queueing": {"rhythm": 0.6},
    "feedback loops": {"rhythm": 0.4},
    "after action review": {"critique": 0.7},
    "mental simulation chosen option": {"critique": 0.75, "story": 0.4},
    "occasion poem verse fable as formats": {"story": 0.75, "emotion": 0.6},
    "classical verse screen": {"rhythm": 0.8},
    "beautiful question": {"hook": 0.8},
    "how might we": {"hook": 0.5, "contrast": 0.4},
    "pareto principle": {"rhythm": 0.4},
    "via negativa": {"rhythm": 0.6, "critique": 0.6},
    "essentialism": {"rhythm": 0.55, "story": 0.5},
}


MANUAL_N = {norm(k): v for k, v in MANUAL.items()}


def video_tags(key: str, text: str) -> dict:
    low = text.lower()
    tags = {}
    for tag, words in TAG_WORDS.items():
        hits = sum(1 for w in words if w in low)
        if hits:
            tags[tag] = round(min(0.6, 0.15 * hits + 0.1), 2)
    for tag, w in MANUAL_N.get(key, {}).items():
        tags[tag] = max(tags.get(tag, 0), w)
    return {t: tags[t] for t in TAGS if t in tags}


# ---------------------------------------------------------------- loaders

def _load(name: str):
    return json.loads(SOURCES[name].read_text(encoding="utf-8"))


def _rel(p: Path) -> str:
    return str(p.relative_to(C.ROOT))


def rows_dragon_mind() -> list:
    out = []
    for f in _load("dragon-mind")["frameworks"]:
        out.append({"source": "dragon-mind", "id": f["id"], "name_en": f["name_en"], "name_ar": f.get("name_ar", ""),
                    "stage": f["stage"], "key": norm(f["id"].replace("-", " ")),
                    "question": (f.get("questions_ar") or f.get("questions_en") or [""])[0],
                    "output": f.get("output", ""), "check": f.get("check", ""),
                    "trap": f.get("anti_pattern") or f.get("trap", ""),
                    "triggers": (f.get("triggers_en") or []) + (f.get("triggers_ar") or []),
                    "text": " ".join([f["name_en"], f.get("output", ""), f.get("summary_en", ""),
                                      " ".join(f.get("triggers_en") or [])])})
    return out


def rows_thinking_books() -> list:
    out = []
    for m in _load("thinking-books")["methods"]:
        out.append({"source": "thinking-books", "id": m["id"], "name_en": m["name_en"], "name_ar": m.get("name_ar", ""),
                    "stage": TB_STAGE.get(m["stage"], "frame"), "key": norm(m["name_en"]),
                    "question": m.get("use_when", ""), "output": (m.get("steps") or [""])[-1],
                    "check": m.get("check", ""), "trap": m.get("trap", ""), "steps": m.get("steps", []),
                    "triggers": m.get("triggers", []),
                    "text": " ".join([m["name_en"], m.get("use_when", ""), " ".join(m.get("steps", []))])})
    return out


def rows_book_methods() -> list:
    out = []
    for m in _load("book-methods")["methods"]:
        out.append({"source": "book-methods", "id": m["id"], "name_en": m["name_en"], "name_ar": m.get("name_ar", ""),
                    "stage": BM_DOMAIN.get(m["domain"], "build"), "key": norm(m["name_en"]),
                    "question": m.get("use_when", ""), "output": (m.get("steps") or [""])[-1],
                    "check": m.get("check", ""), "trap": "", "steps": m.get("steps", []), "triggers": [],
                    "text": " ".join([m["name_en"], m.get("use_when", ""), " ".join(m.get("steps", [])),
                                      m.get("kosif_hook", "")])})
    return out


def rows_mental_models() -> list:
    out = []
    for m in _load("mental-models"):
        out.append({"source": "mental-models", "id": m["id"], "name_en": m["name_en"], "name_ar": m.get("name_ar", ""),
                    "stage": MM_DISCIPLINE.get(m.get("discipline", ""), "frame"), "key": norm(m["name_en"]),
                    "question": m.get("question", ""), "output": m.get("output", ""), "check": "",
                    "trap": m.get("pitfall", ""), "steps": m.get("steps", []), "triggers": m.get("triggers", []),
                    "text": " ".join([m["name_en"], m.get("question", ""), m.get("output", ""),
                                      " ".join(m.get("steps", []))])})
    return out


LOADERS = {"dragon-mind": rows_dragon_mind, "thinking-books": rows_thinking_books,
           "book-methods": rows_book_methods, "mental-models": rows_mental_models}
PRIORITY = list(LOADERS)   # dragon-mind wins the stage and the main text when sources disagree


def build() -> dict:
    counts_before, merged = {}, {}
    for src in PRIORITY:
        rows = LOADERS[src]()
        counts_before[src] = len(rows)
        for r in rows:
            key = ALIASES.get(r["key"], r["key"])
            e = merged.get(key)
            ref = {"source": src, "id": r["id"], "file": _rel(SOURCES[src]), "name_en": r["name_en"]}
            if e is None:
                stage = STAGE_OVERRIDE.get(key, r["stage"]) if src != "dragon-mind" else r["stage"]
                e = merged[key] = {
                    "key": key, "id": r["id"] if src == "dragon-mind" else key.replace(" ", "-"), "name_en": r["name_en"], "name_ar": r["name_ar"],
                    "stage": stage, "stages_seen": [], "question": r["question"], "output": r["output"],
                    "check": r["check"], "trap": r["trap"], "steps": r.get("steps", [])[:5],
                    "triggers": [], "sources": [], "_text": ""}
            e["sources"].append(ref)
            if r["stage"] not in e["stages_seen"]:
                e["stages_seen"].append(r["stage"])
            for k in ("name_ar", "question", "output", "check", "trap"):
                if not e[k] and r.get(k):
                    e[k] = r[k]
            if not e["steps"] and r.get("steps"):
                e["steps"] = r["steps"][:5]
            for t in r["triggers"]:
                if t not in e["triggers"]:
                    e["triggers"].append(t)
            e["_text"] += " " + r["text"]
    entries = []
    for key in sorted(merged):
        e = merged[key]
        tags = video_tags(key, e.pop("_text") + " " + key)
        e["triggers"] = e["triggers"][:16]
        e["video"] = {"tags": tags, "weight": round(max(tags.values()), 2) if tags else 0.0}
        entries.append(e)
    by_stage = {s: sum(1 for e in entries if e["stage"] == s) for s in STAGES}
    multi = sum(1 for e in entries if len({r["source"] for r in e["sources"]}) > 1)
    return {
        "schema": "kosif.dm.mind_registry.v1",
        "about": "سجل واحد لأطر التفكير من أربع مصادر، من غير تكرار، كل إطار على مرحلة من مراحل عقل التنين الست، "
                 "ومعاه وزن للمونتاج (هوك، قصة، إيقاع، إحساس، تناقض، نقد). البناء: scripts/build_mind_registry.py",
        "stages": STAGES, "video_tags": TAGS,
        "sources": {k: _rel(v) for k, v in SOURCES.items()},
        "counts": {"before": counts_before, "before_total": sum(counts_before.values()), "after": len(entries),
                   "merged_away": sum(counts_before.values()) - len(entries), "multi_source": multi,
                   "by_stage": by_stage,
                   "video_relevant": sum(1 for e in entries if e["video"]["weight"] >= 0.5)},
        "frameworks": entries,
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="compare a fresh build with the file on disk")
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args(argv)
    reg = build()
    text = json.dumps(reg, ensure_ascii=False, indent=1) + "\n"
    if a.check:
        same = Path(a.out).exists() and Path(a.out).read_text(encoding="utf-8") == text
        print("up to date" if same else "STALE: rerun build_mind_registry.py")
        return 0 if same else 1
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(text, encoding="utf-8")
    c = reg["counts"]
    print(f"before: {c['before']} = {c['before_total']}")
    print(f"after dedupe: {c['after']} (merged away {c['merged_away']}, {c['multi_source']} from 2+ sources)")
    print(f"by stage: {c['by_stage']} · video-relevant (>=0.5): {c['video_relevant']}")
    print(f"wrote {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
