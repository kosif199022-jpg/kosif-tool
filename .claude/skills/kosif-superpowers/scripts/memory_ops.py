#!/usr/bin/env python3
"""Memory ops: decide ADD, UPDATE, DELETE or NOOP for each new fact against a local memory file / عمليات الذاكرة.

A long-term memory that only appends grows contradictions. This tool compares every candidate fact with what the
store already holds and proposes one operation per fact, with the reason, before anything is written:

    ADD     nothing similar is stored
    UPDATE  same subject and attribute with a new value, or a close restatement that adds detail (the old text goes to history)
    DELETE  the fact retracts a stored one ("no longer", "لم يعد", or op: forget)
    NOOP    already known (near-duplicate)

    python3 scripts/memory_ops.py propose --store memory.json --facts facts.json [--out plan.json]
    python3 scripts/memory_ops.py apply --store memory.json --plan plan.json        # writes the store; history keeps every old value
    python3 scripts/memory_ops.py search --store memory.json "<query>" [--top 5]
    python3 scripts/memory_ops.py --self-test

facts.json: [{"text": "...", "subject": "user", "attribute": "dialect", "value": "Egyptian", "op": "forget"?, "source": "..."}]
(subject/attribute/value are optional; without them the decision uses word overlap only). Facts that contain a secret are
refused. Local files only, opt-in, deterministic; nothing is sent anywhere. The add/update/delete/noop decision step is
the method of mem0 (Apache-2.0), restated and implemented here with plain word overlap instead of an LLM.
Python 3.8+ standard library only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
try:
    from _secrets import find_secrets  # noqa: E402
except ImportError:  # pragma: no cover - the skill ships _secrets.py
    def find_secrets(text):
        return []

DUP = 0.85          # word-overlap at or above this is the same fact
RELATED = 0.5       # at or above this a longer restatement updates the stored one
RETRACT = re.compile(r"\b(no longer|not anymore|stopped|doesn't .* anymore|isn't .* anymore|forget)\b|لم يعد|لم تعد|مبقاش|ماعادش|بطّل|بطل|انسَ|انس ", re.I)
AR_DIAC = re.compile(r"[ً-ٰٟـ]")
STOP = {"the", "a", "an", "is", "are", "was", "were", "to", "of", "and", "or", "in", "on", "for", "with", "that", "this",
        "it", "be", "as", "at", "by", "user", "users", "في", "من", "على", "إلى", "الى", "عن", "و", "أن", "ان", "هو", "هي", "ده", "دي"}


def norm(text: str) -> list:
    t = AR_DIAC.sub("", text.lower())
    t = re.sub("[إأآا]", "ا", t).replace("ى", "ي").replace("ة", "ه")
    words = re.findall(r"[\w']+", t)
    out = []
    for w in words:
        if w.startswith("ال") and len(w) > 4:
            w = w[2:]
        if w not in STOP and len(w) > 1:
            out.append(w)
    return out


def overlap(a: str, b: str) -> float:
    x, y = set(norm(a)), set(norm(b))
    if not x or not y:
        return 0.0
    return len(x & y) / len(x | y)


def contains(a: str, b: str) -> float:
    """Share of the shorter text's words found in the longer one."""
    x, y = set(norm(a)), set(norm(b))
    if not x or not y:
        return 0.0
    small, big = (x, y) if len(x) <= len(y) else (y, x)
    return len(small & big) / len(small)


def mem_id(text: str) -> str:
    return "m-" + hashlib.sha256(" ".join(norm(text)).encode("utf-8")).hexdigest()[:10]


def load_store(path: Path) -> dict:
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"schema": "kosif.memory.v1", "memories": [], "history": []}


def decide(store: dict, fact: dict) -> dict:
    text = (fact.get("text") or "").strip()
    if not text:
        return {"op": "REFUSE", "reason": "empty fact", "fact": fact}
    if find_secrets(text) or find_secrets(json.dumps(fact, ensure_ascii=False)):
        return {"op": "REFUSE", "reason": "the fact contains a secret; store a reference to where it lives instead", "fact": {"text": "[redacted]"}}
    mems = store.get("memories", [])
    subj, attr, val = fact.get("subject"), fact.get("attribute"), fact.get("value")
    retract = fact.get("op") == "forget" or bool(RETRACT.search(text))
    if subj and attr:
        for m in mems:
            if m.get("subject") == subj and m.get("attribute") == attr:
                if retract:
                    return {"op": "DELETE", "target": m["id"], "reason": f"retracts {subj}.{attr}", "fact": fact}
                if str(m.get("value")) == str(val):
                    return {"op": "NOOP", "target": m["id"], "reason": f"{subj}.{attr} is already {val}", "fact": fact}
                return {"op": "UPDATE", "target": m["id"], "reason": f"{subj}.{attr}: {m.get('value')} → {val}", "fact": fact}
    scored = sorted(((overlap(text, m["text"]), contains(text, m["text"]), m) for m in mems), key=lambda t: (-t[0], -t[1], t[2]["id"]))
    if scored:
        ov, cn, m = scored[0]
        if retract and (cn >= RELATED or ov >= RELATED * 0.6):
            return {"op": "DELETE", "target": m["id"], "reason": f"retracts a stored fact (overlap {ov:.2f})", "fact": fact}
        if ov >= DUP:
            return {"op": "NOOP", "target": m["id"], "reason": f"near-duplicate (overlap {ov:.2f})", "fact": fact}
        if cn >= 0.8 and len(norm(text)) > len(norm(m["text"])):
            return {"op": "UPDATE", "target": m["id"], "reason": f"restates with more detail (contains {cn:.2f})", "fact": fact}
        if cn >= 0.8:
            return {"op": "NOOP", "target": m["id"], "reason": f"already covered by a fuller memory (contains {cn:.2f})", "fact": fact}
        if ov >= RELATED:
            return {"op": "UPDATE", "target": m["id"], "reason": f"related restatement (overlap {ov:.2f})", "fact": fact}
    if retract:
        return {"op": "NOOP", "reason": "retraction of something not stored", "fact": fact}
    return {"op": "ADD", "reason": "nothing similar is stored", "fact": fact}


def propose(store: dict, facts: list) -> dict:
    work = json.loads(json.dumps(store))
    plan = []
    for f in facts:
        d = decide(work, f)
        plan.append(d)
        _apply_one(work, d, when="(proposed)")  # later facts see earlier decisions
    counts = {}
    for d in plan:
        counts[d["op"]] = counts.get(d["op"], 0) + 1
    return {"schema": "kosif.memory.plan.v1", "counts": counts, "plan": plan}


def _apply_one(store: dict, d: dict, when: str) -> None:
    mems, hist = store.setdefault("memories", []), store.setdefault("history", [])
    f = d.get("fact", {})
    if d["op"] == "ADD":
        rec = {"id": mem_id(f["text"]), "text": f["text"], "updated": when}
        for k in ("subject", "attribute", "value", "source", "tags"):
            if k in f:
                rec[k] = f[k]
        if all(m["id"] != rec["id"] for m in mems):
            mems.append(rec)
    elif d["op"] in ("UPDATE", "DELETE"):
        for i, m in enumerate(mems):
            if m["id"] == d["target"]:
                hist.append({"op": d["op"], "id": m["id"], "old": m, "reason": d["reason"], "when": when})
                if d["op"] == "DELETE":
                    mems.pop(i)
                else:
                    new = dict(m, text=f["text"], updated=when)
                    for k in ("subject", "attribute", "value", "source", "tags"):
                        if k in f:
                            new[k] = f[k]
                    mems[i] = new
                break


def apply(store: dict, plan: dict, when: str) -> dict:
    out = json.loads(json.dumps(store))
    for d in plan["plan"]:
        if d["op"] in ("ADD", "UPDATE", "DELETE"):
            _apply_one(out, d, when)
    out["memories"].sort(key=lambda m: m["id"])
    return out


def search(store: dict, query: str, top: int = 5) -> list:
    mems = store.get("memories", [])
    docs = [norm(m["text"] + " " + str(m.get("value", ""))) for m in mems]
    q = norm(query)
    n = len(docs) or 1
    avg = sum(len(d) for d in docs) / n if docs else 1
    df = {}
    for d in docs:
        for w in set(d):
            df[w] = df.get(w, 0) + 1
    scored = []
    for m, d in zip(mems, docs):
        s = 0.0
        for w in q:
            tf = d.count(w)
            if tf:
                idf = math.log(1 + (n - df[w] + 0.5) / (df[w] + 0.5))
                s += idf * tf * 2.2 / (tf + 1.2 * (0.25 + 0.75 * len(d) / avg))
        if s > 0:
            scored.append((round(s, 4), m["id"], m["text"]))
    return [{"score": s, "id": i, "text": t} for s, i, t in sorted(scored, key=lambda x: (-x[0], x[1]))[:top]]


def self_test() -> int:
    bad = []
    store = {"schema": "kosif.memory.v1", "memories": [], "history": []}
    facts = [
        {"text": "The user prefers Egyptian Arabic in replies", "subject": "user", "attribute": "dialect", "value": "Egyptian"},
        {"text": "Final videos are exported at 1080x1920 for TikTok"},
        {"text": "Final videos are exported at 1080x1920 for TikTok"},
        {"text": "The user prefers Gulf Arabic in replies", "subject": "user", "attribute": "dialect", "value": "Gulf"},
        {"text": "Final videos are exported at 1080x1920 for TikTok with burned-in Arabic captions"},
        {"text": "The user no longer wants background music in reels"},
        {"text": "api_key = " + "sk-" + "Q7" * 14},
        {"text": "المستخدم يحب خط الرقعة في العناوين"},
    ]
    p = propose(store, facts)
    ops = [d["op"] for d in p["plan"]]
    want = ["ADD", "ADD", "NOOP", "UPDATE", "UPDATE", "NOOP", "REFUSE", "ADD"]
    if ops != want:
        bad.append(("ops", ops))
    s2 = apply(store, p, "2026-10-23")
    if len(s2["memories"]) != 3 or len(s2["history"]) != 2:
        bad.append(("apply", len(s2["memories"]), len(s2["history"])))
    if any("sk-" in json.dumps(s2) for _ in [0]):
        bad.append("secret stored")
    music = {"text": "The user wants calm background music in reels"}
    s3 = apply(s2, propose(s2, [music]), "d")
    p4 = propose(s3, [{"text": "The user no longer wants background music in reels"}])
    if p4["plan"][0]["op"] != "DELETE":
        bad.append(("delete", p4["plan"][0]))
    if search(s2, "dialect Arabic replies")[0]["text"].find("Gulf") < 0:
        bad.append(("search", search(s2, "dialect Arabic replies")))
    if overlap("الخطوط العربية الجميلة", "خطوط عربية جميلة") < 0.6:
        bad.append("arabic normalisation")
    if propose(store, facts) != propose(store, facts):
        bad.append("determinism")
    for b in bad:
        print("FAIL", b)
    print("self-test OK" if not bad else f"self-test: {len(bad)} failure(s)")
    return 1 if bad else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--self-test", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("propose")
    p.add_argument("--store", required=True, type=Path)
    p.add_argument("--facts", required=True, type=Path)
    p.add_argument("--out", type=Path)
    a_ = sub.add_parser("apply")
    a_.add_argument("--store", required=True, type=Path)
    a_.add_argument("--plan", required=True, type=Path)
    a_.add_argument("--when", default="", help="a date label for history entries (default: the plan file's name)")
    s = sub.add_parser("search")
    s.add_argument("--store", required=True, type=Path)
    s.add_argument("query")
    s.add_argument("--top", type=int, default=5)
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if a.cmd == "propose":
        plan = propose(load_store(a.store), json.loads(a.facts.read_text(encoding="utf-8")))
        txt = json.dumps(plan, ensure_ascii=False, indent=1) + "\n"
        if a.out:
            a.out.write_text(txt, encoding="utf-8")
            print(f"wrote {a.out}: {plan['counts']}")
        else:
            print(txt, end="")
        return 0
    if a.cmd == "apply":
        plan = json.loads(a.plan.read_text(encoding="utf-8"))
        out = apply(load_store(a.store), plan, a.when or a.plan.name)
        a.store.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"wrote {a.store}: {len(out['memories'])} memories, {len(out['history'])} history entries")
        return 0
    if a.cmd == "search":
        print(json.dumps(search(load_store(a.store), a.query, a.top), ensure_ascii=False, indent=1))
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
