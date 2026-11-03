#!/usr/bin/env python3
"""KOSIF Dragon Mind: the thinking brain of the Black Dragon, as one super-skill.

It does four things over EVERY Black Dragon catalog entry (skills, powers, tools,
superpowers, styles, playbooks, protocol rules):

  decompose  split each entry into atomic faculties (perceive, transcribe, animate,
             grade colour, verify, ...) with the media kinds it reads and writes
  readiness  measure how the dragon can really use each entry, as a tier:
             T4 executable (reviewed adapter) > T3 runnable (CLI exists) >
             T2 guided (skill/protocol file) > T1 method (knowledge card) > T0 broken
  fuse       fold all entries into ~26 super-faculties, each with its champions
             (strongest usable members) and an honest gap list
  think      run the six-step cognitive cycle on a task: pick thinking and product
             frameworks (distilled from a measured book corpus), architecture
             patterns (measured on GitHub repositories), build a typed handoff
             graph of faculties -> champion capabilities, and criticise it

It never executes catalog tools (only `readiness --probe` runs `--help` through the
Black Dragon's own probe), never spends, uploads or publishes, and never reports a
planned or probed entry as executed. Execution stays with `black_dragon.py run`.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL_DIR = HERE.parent
DATA = SKILL_DIR / "data"
SUPER = SKILL_DIR.parent / "kosif-superpowers"
REPO = SKILL_DIR.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(1, str(SUPER / "scripts"))

import _mind_vocab as V  # noqa: E402

SCHEMA = "kosif.dragon-mind.v1"
CHAMPIONS = 8
MIN_TRIGGER = 0.34  # one trigger shared by at most three frameworks
ALWAYS = ("reason-plan", "verify-qa", "safety-rights", "deliver-publish", "memory-learn")
STAGE_DEFAULTS = {"frame": "first-principles", "explore": "scamper", "decide": "expected-value",
                  "build": "mvp", "verify": "pre-mortem", "learn": "after-action-review"}


# --------------------------------------------------------------------------- inventory

def _dragon():
    import black_dragon as bd  # the Black Dragon itself, read-only
    import _black_dragon_brain as brain
    return bd, brain


def _frontmatter(path: Path) -> dict:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return {}
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    block = text[3:end if end > 0 else 0].strip()
    if block.startswith("{"):  # JSON is valid YAML flow style
        try:
            data = json.loads(block)
            return {k: str(v) for k, v in data.items() if isinstance(v, (str, int, float))}
        except ValueError:
            pass
    out, last = {}, None
    for line in block.splitlines():
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            last = m.group(1)
            out[last] = m.group(2).strip().strip('"')
        elif last and line[:1] in (" ", "\t") and line.strip():  # YAML folded/indented value
            val = out[last].lstrip(">|-").strip()
            out[last] = (val + " " + line.strip()).strip()
    return out


def load_inventory() -> tuple[dict, dict, dict, dict]:
    """(inventory, descriptions, adapters, tool records) straight from the Black Dragon."""
    bd, brain = _dragon()
    inventory = bd.full_inventory()
    desc = brain.metadata(inventory, bd.audit.SKILL)
    for key, meta in inventory.items():
        if meta.get("kind") == "skill":
            fm = _frontmatter(bd.audit.SKILL.parent / meta["source"])
            desc[key] = " ".join([fm.get("name", ""), fm.get("description", "")]).strip()
    adapters = bd._load_adapters(bd.REVIEWED_ADAPTERS)
    return inventory, desc, adapters, bd._tool_records()


def fingerprint(inventory: dict) -> str:
    return hashlib.sha256(json.dumps(sorted(inventory), ensure_ascii=False).encode()).hexdigest()


# --------------------------------------------------------------------------- decompose

_KW = {fid: [(k, re.compile(r"(?<![a-z0-9])" + re.escape(k)) if re.match(r"[a-z0-9]", k) else None)
             for k in V.FACULTY[fid]["kw"]] for fid in V.FACULTY_IDS}


def faculties_of(text: str) -> dict:
    """Distinct keyword stems found: English at a word start, Arabic anywhere (it takes prefixes)."""
    low = text.lower()[:3000]
    hits = {}
    for fid in V.FACULTY_IDS:
        n = sum(1 for k, rx in _KW[fid] if k in low and (rx is None or rx.search(low)))
        if n:
            hits[fid] = n
    return hits


def decompose(inventory: dict, desc: dict) -> dict:
    rows = {}
    for key, meta in inventory.items():
        kind = meta.get("kind") or key.split(":", 1)[0]
        text = " ".join([key.replace("-", " "), desc.get(key, "")])
        hits = faculties_of(text)
        if not hits:  # every entry gets at least one faculty, never dropped
            hits = {{"style": "visual-reference", "protocol": "protocol-govern",
                     "playbook": "protocol-govern", "tool": "code-engineering"}.get(kind, "reason-plan"): 0}
        order = sorted(hits, key=lambda f: (-hits[f], V.FACULTY_IDS.index(f)))
        primary = order[0]
        rows[key] = {"kind": kind, "primary": primary, "faculties": order[:4],
                     "scores": {f: hits[f] for f in order[:4]},
                     "inputs": V.FACULTY[primary]["inputs"], "outputs": V.FACULTY[primary]["outputs"],
                     "stage": V.FACULTY[primary]["stage"]}
    return rows


# --------------------------------------------------------------------------- readiness

def _tier(key: str, meta: dict, desc: str, adapters: dict, tools: dict, bd) -> tuple[str, str]:
    kind = meta.get("kind")
    if key in adapters:
        script = REPO / str(adapters[key].get("script", ""))
        if script.is_file():
            return "T4-executable", "reviewed adapter " + str(adapters[key].get("script"))
        return "T0-broken", "adapter script missing: " + str(adapters[key].get("script"))
    if kind == "tool":
        rec = tools.get(key) or {}
        base = bd.audit.SKILL if rec.get("root") == "skill" else REPO
        target = base / str(rec.get("path", ""))
        if not target.exists():
            return "T0-broken", "tool path missing: " + str(rec.get("path"))
        if rec.get("kind") == "cli":
            if target.suffix == ".py":
                try:
                    has = "argparse" in target.read_text(encoding="utf-8", errors="replace")
                except OSError:
                    has = False
                return ("T3-runnable", "argparse CLI") if has else ("T2-guided", "CLI without argparse")
            return "T3-runnable", "CLI " + target.suffix
        return "T2-guided", "tool kind " + str(rec.get("kind"))
    src = bd._source_path(key, meta)
    if not src.is_file():
        return "T0-broken", "source missing: " + str(meta.get("source"))
    if kind == "skill":
        fm = _frontmatter(src)
        if fm.get("description"):  # Claude falls back to the folder name when name is absent
            return "T2-guided", "SKILL.md with description" + ("" if fm.get("name") else " (name = folder)")
        return "T0-broken", "SKILL.md without a description in its frontmatter"
    if kind in ("protocol", "playbook"):
        return ("T2-guided", "rule file present") if src.stat().st_size > 0 else ("T0-broken", "empty file")
    if len(desc.strip()) >= 12:
        return "T1-method", "described card"
    return "T0-broken", "no usable description"


def readiness(inventory: dict, desc: dict, adapters: dict, tools: dict,
              probe_job: Path | None = None) -> dict:
    bd, _ = _dragon()
    rows = {}
    for key, meta in inventory.items():
        tier, why = _tier(key, meta, desc.get(key, ""), adapters, tools, bd)
        rows[key] = {"tier": tier, "why": why}
    probes = {}
    if probe_job is not None:
        probe_job.mkdir(parents=True, exist_ok=True)
        for key, row in rows.items():
            if row["tier"] == "T3-runnable" and key.startswith("tool:"):
                res = bd._probe(key, tools.get(key), probe_job)
                probes[key] = res.get("status")
                row["probe"] = res.get("status")
                if res.get("status") == "failed":
                    row["tier"], row["why"] = "T0-broken", "probe failed: " + str(res.get("reason") or res.get("exit_code"))
    return {"rows": rows, "tiers": dict(Counter(r["tier"] for r in rows.values())),
            "probes": dict(Counter(probes.values())) if probes else None}


# --------------------------------------------------------------------------- fuse

def fuse(dec: dict, ready: dict, desc: dict) -> dict:
    members = defaultdict(list)
    for key, row in dec.items():
        for f in row["faculties"]:
            members[f].append(key)
    out = {}
    for fid in V.FACULTY_IDS:
        keys = members.get(fid, [])
        tiers = Counter(ready[k]["tier"] for k in keys)

        def rank(k):
            prim = 0 if dec[k]["primary"] == fid else 1
            return (-V.TIER_RANK[ready[k]["tier"]], prim, k)
        champs = [k for k in sorted(keys, key=rank) if ready[k]["tier"] != "T0-broken"][:CHAMPIONS]
        execs = sum(tiers.get(t, 0) for t in ("T4-executable", "T3-runnable"))
        info = V.FACULTY[fid]
        out[fid] = {"ar": info["ar"], "stage": info["stage"], "inputs": info["inputs"],
                    "outputs": info["outputs"], "members": len(keys),
                    "primary_members": sum(1 for k in keys if dec[k]["primary"] == fid),
                    "tiers": dict(sorted(tiers.items())), "executors": execs,
                    "champions": [{"id": k, "tier": ready[k]["tier"]} for k in champs],
                    "external": V.EXTERNAL.get(fid, []),
                    "gap": None if execs else ("no T3/T4 executor in the catalog; external route needs consent: "
                                               + "; ".join(V.EXTERNAL[fid]) if fid in V.EXTERNAL
                                               else "no T3/T4 executor: this faculty is knowledge-only here")}
    return out


def build_map() -> dict:
    inventory, desc, adapters, tools = load_inventory()
    dec = decompose(inventory, desc)
    rd = readiness(inventory, desc, adapters, tools)
    fused = fuse(dec, rd["rows"], desc)
    covered = {k for k in dec}
    return {"schema": SCHEMA + ".map", "inventory_fingerprint": fingerprint(inventory),
            "total": len(inventory), "decomposed": len(covered),
            "by_kind": dict(sorted(Counter(r["kind"] for r in dec.values()).items())),
            "tiers": dict(sorted(rd["tiers"].items())),
            "usable": sum(v for t, v in rd["tiers"].items() if t != "T0-broken"),
            "broken": sorted(k for k, r in rd["rows"].items() if r["tier"] == "T0-broken"),
            "faculties": fused}


# --------------------------------------------------------------------------- think

def _json(name: str, default):
    path = DATA / name
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _tokens(text: str) -> set:
    _, brain = _dragon()
    return brain.tokens(text)


def _stem_in(stem: str, low: str) -> bool:
    """English stems match at a word start ("rate" not in "strategy"); Arabic anywhere (prefixes)."""
    if re.match(r"[a-z0-9]", stem):
        return re.search(r"(?<![a-z0-9])" + re.escape(stem), low) is not None
    return stem in low


def pick_frameworks(task: str, deep: bool) -> list:
    lib = _json("frameworks.json", {}).get("frameworks", [])
    words = _tokens(task)
    low = task.lower()
    trig_of = {fw["id"]: sorted({t.lower() for t in fw.get("triggers_en", []) + fw.get("triggers_ar", [])})
               for fw in lib}
    df = Counter(t for ts in trig_of.values() for t in ts)  # generic triggers ("new") weigh less
    per_stage = defaultdict(list)
    for fw in lib:
        hits = [t for t in trig_of[fw["id"]] if t in words or (len(t) > 3 and _stem_in(t, low))]
        score = round(sum(1.0 / df[t] for t in hits), 3)
        evidence = len(fw.get("book_evidence", []))
        per_stage[fw["stage"]].append((score if score >= MIN_TRIGGER else 0, evidence, fw, hits))
    picked = []
    cap = 2 if deep else 1
    for st in (s["id"] for s in V.CYCLE):
        cands = sorted(per_stage.get(st, []), key=lambda c: (-c[0], -c[1], c[2]["id"]))
        chosen = [c for c in cands if c[0] > 0][:cap]
        if not chosen:
            dflt = [c for c in cands if c[2]["id"] == STAGE_DEFAULTS.get(st)] or cands[:1]
            chosen = dflt[:1]
        for hits, ev, fw, words_hit in chosen:
            picked.append({"id": fw["id"], "name_ar": fw.get("name_ar"), "name_en": fw.get("name_en"),
                           "stage": st, "family": fw.get("family"),
                           "why": ("matches: %s (score %s)" % (", ".join(words_hit), hits)) if hits else "stage default",
                           "questions_ar": fw.get("questions_ar", [])[:3], "output": fw.get("output"),
                           "check": fw.get("check"), "anti_pattern": fw.get("anti_pattern"),
                           "books": [b.get("title") for b in fw.get("source_books", [])],
                           "book_evidence": fw.get("book_evidence", [])[:2]})
    return picked


def pick_patterns(needed: list, consent: bool) -> list:
    pats = _json("github_patterns.json", {}).get("patterns", [])
    builds = sum(1 for f in needed if V.FACULTY[f]["stage"] == "build")
    want = {"planner-executor", "reflection-critic", "typed-schemas", "evaluation"}
    if consent:
        want.add("human-in-the-loop")
    if builds >= 3:
        want.update({"parallel-agents", "dag-workflow"})
    if "research" in needed:
        want.add("rag-retrieval")
    if "memory-learn" in needed:
        want.add("memory")
    out = []
    for p in pats:
        if p["id"] in want:
            out.append({"id": p["id"], "name": p.get("name"), "repos_with_pattern": p.get("repos"),
                        "share": p.get("share"), "exemplars": [e["full_name"] for e in p.get("exemplars", [])[:3]],
                        "mind_feature": p.get("mind_feature"), "implemented": p.get("implemented", False)})
    return out


_TOK: dict = {}


def _entry_tokens(key: str, desc: dict) -> set:
    if key not in _TOK:
        _TOK[key] = _tokens(key.replace("-", " ").replace(":", " ") + " " + desc.get(key, "")[:400])
    return _TOK[key]


def needed_faculties(task: str, dec: dict, desc: dict) -> dict:
    hits = faculties_of(task)
    for f in ALWAYS:
        hits.setdefault(f, 0)
    # Entries that share many words with the task vote for their primary faculty.
    words = _tokens(task)
    votes = Counter()
    if words:
        for key, row in dec.items():
            if len(words & _entry_tokens(key, desc)) >= 3:
                votes[row["primary"]] += 1
    for f, n in votes.most_common(3):
        hits.setdefault(f, 0)
    return {f: hits[f] for f in sorted(hits, key=lambda f: (V.FACULTY_IDS.index(f)))}


def task_champions(fid: str, task_words: set, dec: dict, ready: dict, desc: dict, n: int = 3) -> list:
    """Best members of a faculty for THIS task: task overlap, faculty strength, then usability."""
    scored = []
    for key, row in dec.items():
        if fid not in row["faculties"] or ready[key]["tier"] == "T0-broken":
            continue
        overlap = len(task_words & _entry_tokens(key, desc))
        strength = row["scores"].get(fid, 0) + (2 if row["primary"] == fid else 0)
        tier = V.TIER_RANK[ready[key]["tier"]]
        scored.append((overlap * 3 + strength + tier, overlap, tier, key))
    scored.sort(key=lambda t: (-t[0], -t[2], t[3]))
    picks = [{"id": k, "tier": ready[k]["tier"], "task_overlap": o} for _, o, _, k in scored[:n]]
    best_exec = next(({"id": k, "tier": ready[k]["tier"], "task_overlap": o}
                      for _, o, t, k in scored if t >= 3 and dec[k]["scores"].get(fid, 0) >= 1
                      and (dec[k]["primary"] == fid or o > 0)), None)
    if best_exec and all(p["id"] != best_exec["id"] for p in picks):
        picks.append(best_exec)
    return picks


def think(task: str, deep: bool = False, mind: dict | None = None) -> dict:
    if not task.strip():
        raise ValueError("task cannot be empty")
    inventory, desc, adapters, tools = load_inventory()
    dec = decompose(inventory, desc)
    rd = readiness(inventory, desc, adapters, tools)
    fused = fuse(dec, rd["rows"], desc)
    need = needed_faculties(task, dec, desc)
    task_words = _tokens(task)
    low = task.lower()
    consent = any(w in low for w in V.CONSENT_WORDS)
    stage_order = [s["id"] for s in V.CYCLE]
    nodes = []
    for fid in sorted(need, key=lambda f: (stage_order.index(V.FACULTY[f]["stage"]), V.FACULTY_IDS.index(f))):
        fu = fused[fid]
        champs = task_champions(fid, task_words, dec, rd["rows"], desc)
        best = max((c["tier"] for c in champs), key=lambda t: V.TIER_RANK[t], default="T0-broken")
        nodes.append({"node": "N%d" % (len(nodes) + 1), "faculty": fid, "ar": fu["ar"],
                      "stage": fu["stage"], "inputs": fu["inputs"], "outputs": fu["outputs"],
                      "asked_by_task": need[fid] > 0, "champions": champs, "best_tier": best,
                      "external": fu["external"]})
    # Typed handoffs: each node takes its input from the latest earlier node that produces it.
    edges, issues = [], []
    produced = {"text": "task"}  # the request itself is text
    for n in nodes:
        src = next((produced[k] for k in n["inputs"] if k in produced), None)
        if src is None:
            src = "task"
            issues.append({"node": n["node"], "kind": "handoff",
                           "detail": "no earlier node produces %s; needs an adapter or user material" % "/".join(n["inputs"])})
        edges.append({"from": src, "to": n["node"]})
        for k in n["outputs"]:
            produced[k] = n["node"]
    # Critic: honest gaps.
    for n in nodes:
        if n["stage"] == "build" and V.TIER_RANK[n["best_tier"]] < 3:
            ext = ("; external: " + "; ".join(n["external"])) if n["external"] else ""
            issues.append({"node": n["node"], "kind": "gap",
                           "detail": "%s has no runnable executor (best %s): Claude does it by hand%s" % (n["faculty"], n["best_tier"], ext)})
    if not any(n["faculty"] == "verify-qa" and V.TIER_RANK[n["best_tier"]] >= 3 for n in nodes):
        issues.append({"node": "-", "kind": "verify", "detail": "no runnable verifier on the graph"})
    if consent:
        issues.append({"node": "-", "kind": "consent",
                       "detail": "task mentions spending/publishing: that step waits for the owner's explicit yes"})
    frameworks = pick_frameworks(task, deep)
    patterns = pick_patterns(list(need), consent)
    plan_ids = [c["id"] for n in nodes for c in n["champions"]]
    trace = {"schema": SCHEMA + ".trace", "task": task, "depth": "deep" if deep else "standard",
             "inventory_total": len(inventory), "inventory_fingerprint": fingerprint(inventory),
             "tiers": dict(sorted(rd["tiers"].items())),
             "cycle": V.CYCLE, "frameworks": frameworks, "patterns": patterns,
             "faculties_needed": list(need), "graph": {"nodes": nodes, "edges": edges},
             "critic": issues, "consent_required": consent,
             "handoff": {"focus_ids": plan_ids,
                         "commands": [
                             'python3 .claude/skills/kosif-superpowers/scripts/black_dragon.py plan "%s" --mode pro-max' % task.replace('"', "'"),
                             'python3 .claude/skills/kosif-superpowers/scripts/black_dragon.py run "%s" --job out/black-dragon/<job> --probe-tools --reviewed-adapters' % task.replace('"', "'")]},
             "evidence_rule": "planned != probed != executed; only black_dragon.py run receipts count as executed",
             "limitations": "deterministic lexical planner, not an LLM; frameworks are operators to apply, not proof of quality"}
    trace["digest"] = hashlib.sha256(json.dumps({k: trace[k] for k in ("task", "faculties_needed", "graph", "frameworks")},
                                                ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    return trace


def report_md(trace: dict) -> str:
    L = ["# عقل التنين الأسود — Dragon Mind", "", "**المهمة:** " + trace["task"], "",
         "**المخزون:** %d قدرة · الدرجات: %s" % (trace["inventory_total"],
                                              " · ".join("%s=%d" % kv for kv in trace["tiers"].items())), "",
         "## 1. أطر التفكير المختارة (دورة من ست خطوات)", ""]
    for fw in trace["frameworks"]:
        L.append("- **%s** (%s) — %s · %s · المخرج: %s · الفحص: %s" % (
            fw["name_ar"], fw["stage"], fw["name_en"], fw["why"], fw["output"], fw["check"]))
        for q in fw["questions_ar"]:
            L.append("  - " + q)
    L += ["", "## 2. أنماط معمارية مقاسة على GitHub", ""]
    for p in trace["patterns"]:
        L.append("- **%s** — في %s مستودع (%s) · مطبّق في العقل: %s · أمثلة: %s" % (
            p["name"], p["repos_with_pattern"], p["share"], "نعم" if p["implemented"] else "لا",
            ", ".join(p["exemplars"])))
    L += ["", "## 3. رسم التنفيذ (ملكات → أبطال القدرات)", "", "| عقدة | المرحلة | الملكة | أفضل درجة | الأبطال |", "|---|---|---|---|---|"]
    for n in trace["graph"]["nodes"]:
        L.append("| %s | %s | %s | %s | %s |" % (n["node"], n["stage"], n["ar"], n["best_tier"],
                                               ", ".join("`%s`" % c["id"] for c in n["champions"])))
    L += ["", "## 4. الناقد", ""]
    L += ["- [%s] %s: %s" % (i["kind"], i["node"], i["detail"]) for i in trace["critic"]] or ["- لا ملاحظات"]
    L += ["", "## 5. التسليم للتنين الأسود", ""] + ["```", *trace["handoff"]["commands"], "```", "",
          "> " + trace["evidence_rule"], "", "digest: `%s`" % trace["digest"], ""]
    return "\n".join(L)


# --------------------------------------------------------------------------- upgrade

def upgrade_plan(max_executors: int = 12) -> dict:
    """Faculties with few runnable executors, each with the measured repos that could close the gap.

    A candidate is a lead to review (license, safety, fit), never an install or a claim of capability.
    """
    m = build_map()
    cands = _json("github_patterns.json", {}).get("faculty_candidates", {})
    weak = []
    for fid, info in sorted(m["faculties"].items(), key=lambda kv: (kv[1]["executors"], kv[0])):
        if info["executors"] > max_executors:
            continue
        c = cands.get(fid, {})
        weak.append({"faculty": fid, "ar": info["ar"], "members": info["members"], "executors": info["executors"],
                     "external": info["external"], "github_matching_repos": c.get("matching_repos"),
                     "candidates": [r for r in c.get("top", []) if r.get("permissive")][:5],
                     "next_step": "review one permissive candidate, wrap it as a CLI in data/tools.json, "
                                  "add a reviewed adapter, prove it with a receipt"})
    return {"schema": SCHEMA + ".upgrade", "threshold": max_executors, "weak_faculties": weak,
            "rule": "candidates are leads, not installed capabilities; nothing is downloaded or installed"}


# --------------------------------------------------------------------------- doctor

def doctor() -> dict:
    checks = []
    fw = _json("frameworks.json", {}).get("frameworks", [])
    checks.append(("frameworks", len(fw) >= 100 and len({f["id"] for f in fw}) == len(fw), "%d frameworks" % len(fw)))
    gp = _json("github_patterns.json", {})
    checks.append(("github_patterns", bool(gp.get("patterns")), "%s repos measured" % gp.get("repos_measured")))
    bk = _json("books_thinking.json", {})
    checks.append(("books", bool(bk.get("books")), "%s screened, %s kept" % (bk.get("screened"), len(bk.get("books", [])))))
    snap = _json("mind_map.json", {})
    try:
        inventory, *_ = load_inventory()
        live = fingerprint(inventory)
        checks.append(("black_dragon_inventory", True, "%d entries" % len(inventory)))
        checks.append(("mind_map_fresh", snap.get("inventory_fingerprint") == live,
                       "snapshot matches live inventory" if snap.get("inventory_fingerprint") == live
                       else "stale snapshot: run `dragon_mind.py fuse --write`"))
    except Exception as exc:  # noqa: BLE001 - doctor reports, never crashes
        checks.append(("black_dragon_inventory", False, str(exc)[:200]))
    return {"ok": all(c[1] for c in checks if c[0] != "mind_map_fresh"),
            "checks": [{"check": c[0], "pass": c[1], "detail": c[2]} for c in checks]}


# --------------------------------------------------------------------------- cli

def _dump(obj, path: Path | None):
    text = json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=False) + "\n"
    if path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("decompose", help="faculties of every catalog entry")
    d.add_argument("--out", type=Path)
    r = sub.add_parser("readiness", help="usability tier of every entry (static; --probe runs --help)")
    r.add_argument("--out", type=Path)
    r.add_argument("--probe", type=Path, metavar="JOB_DIR", help="also run the dragon's --help probe on T3 tools")
    f = sub.add_parser("fuse", help="fold everything into super-faculties")
    f.add_argument("--write", action="store_true", help="write data/mind_map.json")
    f.add_argument("--check", action="store_true", help="exit 1 if data/mind_map.json is stale")
    t = sub.add_parser("think", help="run the cognitive cycle on a task")
    t.add_argument("task")
    t.add_argument("--deep", action="store_true", help="two frameworks per stage instead of one")
    t.add_argument("--out", type=Path, help="work dir for mind_trace.json and mind_report.md")
    sub.add_parser("doctor", help="read-only health check")
    up = sub.add_parser("upgrade", help="weakest faculties + measured GitHub candidates to strengthen them")
    up.add_argument("--max-executors", type=int, default=12)
    ad = sub.add_parser("adapters", help="write reviewed adapters + the mind's own adapter for black_dragon.py --adapters")
    ad.add_argument("--out", type=Path, required=True)
    a = ap.parse_args(argv)
    if a.cmd == "decompose":
        inv, desc, _, _ = load_inventory()
        rows = decompose(inv, desc)
        _dump({"schema": SCHEMA + ".decompose", "total": len(inv), "decomposed": len(rows),
               "primary": dict(Counter(r["primary"] for r in rows.values()).most_common()),
               "rows": rows} if a.out else
              {"total": len(inv), "decomposed": len(rows),
               "primary": dict(Counter(r["primary"] for r in rows.values()).most_common())}, a.out)
        return 0
    if a.cmd == "readiness":
        inv, desc, ad, tools = load_inventory()
        rd = readiness(inv, desc, ad, tools, a.probe)
        summary = {"total": len(inv), "tiers": dict(sorted(rd["tiers"].items())), "probes": rd["probes"],
                   "broken": sorted(k for k, v in rd["rows"].items() if v["tier"] == "T0-broken")}
        _dump({**summary, "rows": rd["rows"]} if a.out else summary, a.out)
        return 0
    if a.cmd == "fuse":
        m = build_map()
        target = DATA / "mind_map.json"
        text = json.dumps(m, ensure_ascii=False, indent=1) + "\n"
        if a.check:
            ok = target.is_file() and target.read_text(encoding="utf-8") == text
            print("mind_map.json " + ("fresh" if ok else "STALE"))
            return 0 if ok else 1
        if a.write:
            target.write_text(text, encoding="utf-8")
            print("wrote %s (%d entries, %d faculties)" % (target.relative_to(REPO), m["total"], len(m["faculties"])))
        else:
            sys.stdout.write(json.dumps({k: m[k] for k in ("total", "decomposed", "tiers", "usable")} |
                                        {"faculties": {k: {"members": v["members"], "executors": v["executors"]}
                                                       for k, v in m["faculties"].items()}},
                                        ensure_ascii=False, indent=1) + "\n")
        return 0
    if a.cmd == "think":
        tr = think(a.task, a.deep)
        if a.out:
            a.out.mkdir(parents=True, exist_ok=True)
            (a.out / "mind_trace.json").write_text(json.dumps(tr, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
            (a.out / "mind_report.md").write_text(report_md(tr), encoding="utf-8")
            print("wrote %s/mind_trace.json and mind_report.md (digest %s)" % (a.out, tr["digest"][:12]))
        else:
            sys.stdout.write(report_md(tr))
        return 0
    if a.cmd == "upgrade":
        _dump(upgrade_plan(a.max_executors), None)
        return 0
    if a.cmd == "adapters":
        bd, _ = _dragon()
        merged = dict(bd._load_adapters(bd.REVIEWED_ADAPTERS))
        merged[V.MIND_ADAPTER_KEY] = V.MIND_ADAPTER
        _dump({"_comment": "Reviewed Black Dragon adapters plus the Dragon Mind (read-only think). "
                           "Use: black_dragon.py run TASK --job out/black-dragon/<job> --adapters THIS --execute-adapters",
               "adapters": merged}, a.out)
        print("wrote %s (%d adapters)" % (a.out, len(merged)))
        return 0
    if a.cmd == "doctor":
        res = doctor()
        _dump(res, None)
        return 0 if res["ok"] else 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
