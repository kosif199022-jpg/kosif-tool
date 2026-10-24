#!/usr/bin/env python3
"""Cumulative research memory and source registry for KOSIF Infinite Matrices.

ledger  memory/ledger.jsonl — append-only, hash-chained (each line stores the sha256 of the
        previous line), committed to git so later sessions build on saved results.
        Event types: experiment, replication, idea, rating, hypothesis_status.
sources sources/registry.json — every file or link that fed the work, by sha256, with its
        rights, relevance and what it was used for. Same bytes under another name become an
        alias, never a second source.

Rules enforced here (not just documented):
  * the same recipe hash cannot be recorded twice as an "experiment"; a re-run is a "replication";
  * an idea whose parent/role signature already exists (in the 283 seeds or the ledger) is refused;
  * a rating must name an experiment that exists in the ledger;
  * a hypothesis can leave UNTESTED_UNRENDERED only with an evidence file whose sha256 is stored.
"""
import datetime
import hashlib
import json
import math
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
LEDGER = SKILL / "memory" / "ledger.jsonl"
REGISTRY = SKILL / "sources" / "registry.json"
SEEDS = SKILL / "data" / "283_hypothesis_seeds.json"
EVENT_TYPES = ("experiment", "replication", "idea", "rating", "hypothesis_status")
HYP_STATUSES = ("UNTESTED_UNRENDERED", "PROPOSED_RECIPE", "NUMERIC_TESTED", "RENDER_TESTED", "REJECTED", "PRODUCTION_READY")
RELEVANCE = ("core", "method", "context", "not_relevant")


def now_iso():
    return datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


# ------------------------------------------------------------------ ledger
def read_ledger(path=LEDGER):
    p = Path(path)
    if not p.exists():
        return []
    return [json.loads(line) for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]


def verify_ledger(path=LEDGER):
    p = Path(path)
    if not p.exists():
        return {"ok": True, "events": 0, "problems": []}
    prev = None
    problems = []
    lines = [l for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    for i, line in enumerate(lines, 1):
        ev = json.loads(line)
        if ev.get("seq") != i:
            problems.append("line %d: seq %s" % (i, ev.get("seq")))
        if ev.get("prev_sha256") != prev:
            problems.append("line %d: broken hash chain" % i)
        if ev.get("type") not in EVENT_TYPES:
            problems.append("line %d: unknown type %s" % (i, ev.get("type")))
        prev = hashlib.sha256(line.encode("utf-8")).hexdigest()
    return {"ok": not problems, "events": len(lines), "head_sha256": prev, "problems": problems}


def append(event, path=LEDGER):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    if event.get("type") not in EVENT_TYPES:
        raise ValueError("type must be one of %s" % (EVENT_TYPES,))
    chk = verify_ledger(p)
    if not chk["ok"]:
        raise RuntimeError("ledger chain is broken, refusing to append: %s" % chk["problems"][:3])
    ev = dict(event)
    ev["seq"] = chk["events"] + 1
    ev["prev_sha256"] = chk.get("head_sha256")
    ev.setdefault("at", now_iso())
    line = canonical(ev)
    with p.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    return ev


def next_id(prefix, events):
    n = sum(1 for e in events if e.get("id", "").startswith(prefix))
    return "%s%04d" % (prefix, n + 1)


def record_experiment(report, artifacts, path=LEDGER, replication=False, sources=None):
    events = read_ledger(path)
    same = [e for e in events if e["type"] == "experiment" and e.get("recipe_hash") == report["recipe_hash"]]
    if same and not replication:
        raise ValueError("recipe %s (hash %s) already recorded as %s; pass replication=True to log a re-run"
                         % (report["recipe_id"], report["recipe_hash"], same[0]["id"]))
    kind = "replication" if same else "experiment"
    ev = {"type": kind, "id": next_id("EXP-", events), "recipe_id": report["recipe_id"], "recipe_hash": report["recipe_hash"],
          "replicates": same[0]["id"] if same else None, "verdict": report["verdict"], "status": report.get("status"),
          "checks": report["checks"], "effect": report["effect"],
          "dose_spearman": report["dose_response"]["spearman_rho"],
          "roles": report.get("roles"), "parents": report.get("parents"),
          "render": report.get("render"), "artifacts": artifacts, "sources": sources or []}
    return append(ev, path)


def seed_signatures(path=SEEDS):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    sigs = set()
    for h in data["hypotheses"]:
        sigs.add(signature([p["style_id"] for p in h["parents"]], h["roles"]))
    return sigs


def signature(parent_ids, roles):
    return "|".join(sorted(parent_ids)) + "#" + ",".join("%s=%s" % (k, roles[k]) for k in sorted(roles))


def known_signatures(path=LEDGER, seeds=SEEDS):
    sigs = seed_signatures(seeds)
    for e in read_ledger(path):
        if e["type"] == "idea":
            sigs.add(e["signature"])
    return sigs


def record_idea(idea, path=LEDGER, seeds=SEEDS):
    sig = signature(idea["parents"], idea["roles"])
    if sig in known_signatures(path, seeds):
        raise ValueError("duplicate idea signature: " + sig)
    ev = {"type": "idea", "id": idea["id"], "signature": sig, "parents": idea["parents"], "roles": idea["roles"],
          "status": "PROPOSED", "origin": idea.get("origin", "ideate")}
    return append(ev, path)


def record_rating(experiment_id, score, by, notes="", path=LEDGER):
    events = read_ledger(path)
    exp = next((e for e in events if e.get("id") == experiment_id and e["type"] in ("experiment", "replication")), None)
    if exp is None:
        raise ValueError("no experiment %s in the ledger" % experiment_id)
    if not (0 <= float(score) <= 5):
        raise ValueError("score must be 0..5")
    if not by or not by.strip():
        raise ValueError("a rating needs the reviewer's name (--by)")
    return append({"type": "rating", "experiment": experiment_id, "recipe_id": exp["recipe_id"], "score": float(score),
                   "by": by.strip(), "notes": notes, "kind": "HUMAN_RATING"}, path)


def mark_hypothesis(hyp_id, status, evidence=None, note="", path=LEDGER, seeds=SEEDS):
    ids = {h["id"] for h in json.loads(Path(seeds).read_text(encoding="utf-8"))["hypotheses"]}
    if hyp_id not in ids:
        raise ValueError("unknown hypothesis id " + hyp_id)
    if status not in HYP_STATUSES:
        raise ValueError("status must be one of %s" % (HYP_STATUSES,))
    ev = {"type": "hypothesis_status", "hypothesis": hyp_id, "status": status, "note": note}
    if status != "UNTESTED_UNRENDERED":
        if not evidence or not Path(evidence).exists():
            raise ValueError("leaving UNTESTED needs an existing --evidence file")
        ev["evidence"] = str(evidence)
        ev["evidence_sha256"] = sha256_file(evidence)
    return append(ev, path)


def hypothesis_status(path=LEDGER, seeds=SEEDS):
    data = json.loads(Path(seeds).read_text(encoding="utf-8"))
    status = {h["id"]: h.get("status", "UNTESTED_UNRENDERED") for h in data["hypotheses"]}
    for e in read_ledger(path):
        if e["type"] == "hypothesis_status":
            status[e["hypothesis"]] = e["status"]
    counts = {}
    for s in status.values():
        counts[s] = counts.get(s, 0) + 1
    return status, counts


def operator_scores(path=LEDGER):
    """Research feedback: Beta(1+wins, 1+losses) per (role, operator) from human ratings
    (score >= 4 is a win) and from experiment verdicts. Untested ideas add nothing."""
    events = read_ledger(path)
    exp = {e["id"]: e for e in events if e["type"] in ("experiment", "replication")}
    recipe_roles = {}
    for e in events:
        if e["type"] in ("experiment", "replication") and e.get("roles"):
            recipe_roles[e["recipe_id"]] = e["roles"]
    wins, losses = {}, {}

    def bump(roles, ok):
        for role, op in (roles or {}).items():
            k = role + ":" + op
            (wins if ok else losses)[k] = (wins if ok else losses).get(k, 0) + 1
    for e in events:
        if e["type"] in ("experiment", "replication"):
            bump(e.get("roles"), e.get("verdict") == "CONFIRMED_IN_MODEL")
        elif e["type"] == "rating":
            bump(recipe_roles.get(e["recipe_id"]) or (exp.get(e["experiment"]) or {}).get("roles"), e["score"] >= 4)
    out = {}
    for k in sorted(set(wins) | set(losses)):
        a, b = 1 + wins.get(k, 0), 1 + losses.get(k, 0)
        out[k] = {"wins": wins.get(k, 0), "losses": losses.get(k, 0), "posterior_mean": round(a / (a + b), 4),
                  "sd": round(math.sqrt(a * b / ((a + b) ** 2 * (a + b + 1))), 4)}
    return out


def stats(path=LEDGER):
    events = read_ledger(path)
    by = {}
    for e in events:
        by[e["type"]] = by.get(e["type"], 0) + 1
    _, hyp = hypothesis_status(path)
    return {"events": len(events), "by_type": by, "chain": verify_ledger(path), "hypotheses_283": hyp,
            "experiments": [{k: e.get(k) for k in ("id", "type", "recipe_id", "verdict", "status", "at")}
                            for e in events if e["type"] in ("experiment", "replication")],
            "operator_scores": operator_scores(path)}


# ------------------------------------------------------------------ source registry
def read_registry(path=REGISTRY):
    p = Path(path)
    if not p.exists():
        return {"schema": "kosif.matrices.sources.v1", "sources": []}
    return json.loads(p.read_text(encoding="utf-8"))


def write_registry(reg, path=REGISTRY):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    reg["sources"].sort(key=lambda s: s["id"])
    p.write_text(json.dumps(reg, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def add_source(title, relevance, rights, used_for, file=None, url=None, name=None, kind=None, note="",
               pages=None, path=REGISTRY, added=None):
    if relevance not in RELEVANCE:
        raise ValueError("relevance must be one of %s" % (RELEVANCE,))
    if not file and not url:
        raise ValueError("a source needs --file or --url")
    reg = read_registry(path)
    digest = sha256_file(file) if file else None
    size = Path(file).stat().st_size if file else None
    display = name or (Path(file).name if file else url)
    for s in reg["sources"]:
        if (digest and s.get("sha256") == digest) or (url and not digest and s.get("url") == url):
            if display not in s["names"]:
                s["names"].append(display)
                write_registry(reg, path)
            return s, False
    n = 1 + max([int(s["id"].split("-")[1]) for s in reg["sources"]] or [0])
    s = {"id": "SRC-%03d" % n, "title": title, "names": [display], "kind": kind or (Path(file).suffix.lstrip(".") if file else "url"),
         "sha256": digest, "bytes": size, "pages": pages, "url": url, "rights": rights, "relevance": relevance,
         "used_for": used_for, "note": note, "added": added or now_iso()[:10],
         "content_in_repo": "none (metadata and derived measurements only)"}
    reg["sources"].append(s)
    write_registry(reg, path)
    return s, True


def verify_source(file, path=REGISTRY):
    digest = sha256_file(file)
    for s in read_registry(path)["sources"]:
        if s.get("sha256") == digest:
            return s
    return None
