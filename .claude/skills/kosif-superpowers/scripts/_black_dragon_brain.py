#!/usr/bin/env python3
"""Deterministic planning brain for ALL Black Dragon catalog entries.

Owner's rule: every capability is used, none is left out. The brain's job is
to decide HOW and WHERE each one is used for this task:

* part   - which part of the job it serves (the seven stages of the capability
           mind map: understand, plan, create, refine, assemble, verify, deliver)
* mode   - how it is applied (execute an adapter, run a tool, follow a skill,
           apply a method, enforce a protocol rule, use as a visual reference,
           or act as a quality gate)
* weight - lead (top entries of its part for this task), core (matches the
           task) or support (no word overlap; still assigned, never dropped)
* application - one line saying what this entry does for this task

Relevance only orders and weights work; it never removes an entry. Dependency
layers are explicit. This planner is not an LLM: it cannot make a documentation
card executable, and an assignment is not proof that anything ran.
"""
from __future__ import annotations
import hashlib
import json
import re
from pathlib import Path

WORDS = re.compile(r"[\w؀-ۿ]+", re.UNICODE)
STOP = {"and", "the", "for", "with", "from", "skill", "tool", "power",
        "من", "في", "على", "الى", "إلى", "مع", "كل", "عن", "ده", "هي"}
# Coarse roles kept for older readers of the plan (analyze/build/verify/support).
STAGES = {
    "analyze": ("think", "reason", "research", "inspect", "audit", "source", "تحليل", "بحث", "مراجعة", "تخطيط"),
    "build": ("render", "design", "edit", "montage", "animation", "video", "motion",
              "صمم", "ارسم", "مونتاج", "فيديو", "برمجة", "توليد", "إنشاء"),
    "verify": ("verify", "test", "check", "quality", "validation", "qa", "تحقق", "اختبار", "جودة"),
}
# Fallback when data/capability_mindmap.json is not available (tests, bare installs).
PARTS = [
    {"id": "understand", "ar": "افهم المادة", "en": "Understand the material",
     "kw": ["analy", "inspect", "detect", "measure", "transcri", "audit", "read", "extract",
            "research", "search", "تحليل", "بحث", "افهم", "قراءة"]},
    {"id": "plan", "ar": "خطّط وقرّر", "en": "Plan and decide",
     "kw": ["plan", "think", "reason", "decide", "strategy", "brief", "script", "story",
            "خطة", "تخطيط", "تفكير", "قرار", "سيناريو"]},
    {"id": "create", "ar": "اصنع", "en": "Create",
     "kw": ["generat", "design", "draw", "animat", "motion", "write", "compose", "build",
            "توليد", "صمم", "ارسم", "تحريك", "إنشاء", "اكتب"]},
    {"id": "refine", "ar": "حسّن واصقل", "en": "Refine and polish",
     "kw": ["edit", "color", "grade", "polish", "improve", "clean", "denois", "upscal",
            "تعديل", "تلوين", "تحسين", "صقل"]},
    {"id": "assemble", "ar": "جمّع وارندر", "en": "Assemble and render",
     "kw": ["render", "montage", "assembl", "encode", "export", "mix", "timeline", "sync",
            "مونتاج", "رندر", "تصدير", "مزج"]},
    {"id": "verify", "ar": "تحقّق", "en": "Verify",
     "kw": ["verify", "test", "check", "quality", "validat", "qa", "proof", "lint",
            "تحقق", "اختبار", "جودة", "فحص"]},
    {"id": "deliver", "ar": "سلّم وانشر", "en": "Deliver and publish",
     "kw": ["deliver", "publish", "upload", "share", "deploy", "package", "report",
            "تسليم", "نشر", "رفع", "تقرير"]},
]
ALWAYS = ("understand", "plan", "verify", "deliver")  # every job needs these parts
MODES = {
    "execute": ("نفّذ بمحوّل مراجَع", "run its reviewed adapter on the task"),
    "run-tool": ("شغّل الأداة", "run this tool on the task's material"),
    "follow-skill": ("اتبع المهارة", "follow this skill's workflow"),
    "apply-method": ("طبّق الطريقة", "apply this method"),
    "protocol-rule": ("التزم بقاعدة البروتوكول", "enforce this protocol rule"),
    "visual-reference": ("استعمله مرجعًا بصريًا", "use as a visual/motion reference"),
    "quality-gate": ("استعمله بوابة جودة", "use as a quality gate"),
}
LEADS_PER_PART = 5


AR_PREFIXES = ("وال", "بال", "لل", "ال", "و", "ب", "ل", "ف")


def tokens(text: str) -> set[str]:
    """Lower-cased words; Arabic words also give their form without a leading و/ب/ال…"""
    out = set()
    for raw in WORDS.findall(text):
        word = raw.lower()
        if len(word) <= 1 or word in STOP:
            continue
        out.add(word)
        if "\u0600" <= word[0] <= "\u06ff":
            for pre in AR_PREFIXES:
                if word.startswith(pre) and len(word) - len(pre) >= 3:
                    out.add(word[len(pre):])
                    break
    return out


def _rows(obj) -> list:
    if isinstance(obj, list):
        return obj
    if isinstance(obj, dict):
        for key in ("powers", "items", "tools", "styles"):
            if isinstance(obj.get(key), list):
                return obj[key]
    return []


def _text(row: dict, keys) -> str:
    out = []
    for k in keys:
        v = row.get(k, "")
        out.append(" ".join(map(str, v)) if isinstance(v, list) else str(v))
    return " ".join(out)


def metadata(index: dict, skill_root: Path) -> dict:
    """Optional registry descriptors for better rankings, not a filter."""
    result = {}
    for file in sorted((skill_root / "data" / "powers").glob("*.json")):
        try:
            for row in _rows(json.loads(file.read_text(encoding="utf-8"))):
                if isinstance(row, dict) and row.get("id") and "power:" + str(row["id"]) in index:
                    result["power:" + str(row["id"])] = _text(row, (
                        "title", "name_en", "name_ar", "ar", "en", "what", "how", "when",
                        "summary", "family", "domain", "tags"))
        except (ValueError, OSError):
            continue
    try:
        for row in _rows(json.loads((skill_root / "data" / "tools.json").read_text(encoding="utf-8"))):
            key = "tool:" + str(row.get("id", ""))
            if key in index:
                result[key] = _text(row, ("title_ar", "title_en", "summary_ar", "summary_en",
                                          "area", "keywords", "use_when"))
    except (OSError, ValueError):
        pass
    try:
        for row in _rows(json.loads((skill_root / "data" / "superpowers.json").read_text(encoding="utf-8"))):
            key = "superpower:" + str(row.get("id", ""))
            if key in index:
                result[key] = _text(row, ("name_en", "name_ar", "domain", "family", "focus"))
    except (OSError, ValueError):
        pass
    for key, meta in index.items():
        if key in result:
            continue
        if meta.get("text"):
            result[key] = str(meta["text"])
    return result


def load_parts(skill_root: Path | None) -> list:
    """The seven parts from the capability mind map, falling back to built-in ones."""
    if skill_root is not None:
        try:
            stages = json.loads((skill_root / "data" / "capability_mindmap.json")
                                .read_text(encoding="utf-8")).get("stages")
            if isinstance(stages, list) and stages and all(
                    isinstance(s, dict) and s.get("id") and isinstance(s.get("kw"), list) for s in stages):
                return [{"id": s["id"], "ar": s.get("ar", s["id"]), "en": s.get("en", s["id"]),
                         "kw": [str(k).lower() for k in s["kw"]]} for s in stages]
        except (OSError, ValueError):
            pass
    return PARTS


def _validate_dependencies(inventory: dict, adapters: dict) -> dict[str, set[str]]:
    deps = {}
    for key in inventory:
        spec = adapters.get(key, {})
        values = spec.get("depends_on", [])
        if not isinstance(values, list) or not all(isinstance(k, str) for k in values):
            raise ValueError("depends_on must be a list of catalog IDs: " + key)
        if len(values) != len(set(values)):
            raise ValueError("Duplicate dependency for: " + key)
        for dep in values:
            if dep not in inventory or dep == key:
                raise ValueError("Invalid dependency for " + key + ": " + dep)
        deps[key] = set(values)
    return deps


def _kind(key: str, meta: dict) -> str:
    return str(meta.get("kind") or key.split(":", 1)[0])


def _part_of(desc: str, parts: list) -> tuple[str, dict]:
    low = desc.lower()
    score = {p["id"]: sum(1 for kw in p["kw"] if kw and kw in low) for p in parts}
    order = [p["id"] for p in parts]
    best = max(order, key=lambda pid: (score[pid], -order.index(pid)))
    if not score[best]:
        best = "plan"  # a capability with no stage words informs the plan
    return best, score


def _mode(kind: str, part: str, has_adapter: bool) -> str:
    if has_adapter:
        return "execute"
    if part == "verify" and kind != "style":
        return "quality-gate"
    return {"tool": "run-tool", "skill": "follow-skill", "style": "visual-reference",
            "protocol": "protocol-rule"}.get(kind, "apply-method")


def _task_parts(task: str, parts: list) -> dict:
    """How strongly the task asks for each part (0 = only by policy)."""
    low = task.lower()
    weights = {p["id"]: sum(1 for kw in p["kw"] if kw and kw in low) for p in parts}
    for pid in ALWAYS:
        if pid in weights:
            weights[pid] = max(weights[pid], 1)
    return weights


def plan(task: str, inventory: dict, adapters: dict, skill_root: Path | None = None) -> dict:
    if not task.strip():
        raise ValueError("Task cannot be empty")
    descriptions = metadata(inventory, skill_root) if skill_root is not None else {}
    parts = load_parts(skill_root)
    part_info = {p["id"]: p for p in parts}
    task_words = tokens(task)
    task_weights = _task_parts(task, parts)
    deps = _validate_dependencies(inventory, adapters)
    scores, roles, part_of, modes, overlap = {}, {}, {}, {}, {}
    for key, meta in inventory.items():
        desc = " ".join((key, str(meta.get("source", "")), descriptions.get(key, "")))
        words = tokens(desc)
        hits = sorted(task_words & words)
        overlap[key] = hits[:6]
        part, _ = _part_of(desc, parts)
        part_of[key] = part
        # Score = shared words with the task, boosted when the task asks for its part.
        scores[key] = len(hits) * 2 + (task_weights.get(part, 0) if hits else 0)
        stage_score = {stage: sum(1 for term in terms if term in desc.lower())
                       for stage, terms in STAGES.items()}
        roles[key] = max(STAGES, key=lambda s: (stage_score[s], -list(STAGES).index(s)))
        if not any(stage_score.values()):
            roles[key] = "support"
        modes[key] = _mode(_kind(key, meta), part, key in adapters)
    # Leads: the strongest entries of each part for this task.
    leads = {}
    for pid in part_info:
        members = sorted((k for k in inventory if part_of[k] == pid), key=lambda k: (-scores[k], k))
        leads[pid] = [k for k in members if scores[k] > 0][:LEADS_PER_PART]
    lead_set = {k for v in leads.values() for k in v}
    # Kahn waves: no dependency may run until all of its prerequisites finished.
    remaining = {k: set(v) for k, v in deps.items()}
    waves, done = [], set()
    while remaining:
        ready = [k for k, pending in remaining.items() if not pending]
        if not ready:
            raise ValueError("Cyclic Black Dragon adapter dependencies")
        order = [p["id"] for p in parts]
        ready.sort(key=lambda k: (order.index(part_of[k]), -scores[k], k))
        waves.append(ready)
        done.update(ready)
        remaining = {k: pending - done for k, pending in remaining.items() if k not in done}
    items = {}
    for key in inventory:
        part, mode = part_of[key], modes[key]
        weight = "lead" if key in lead_set else "core" if scores[key] > 0 else "support"
        info = part_info[part]
        reason = ("matches: " + ", ".join(overlap[key])) if overlap[key] else "no word overlap; assigned by its stage"
        items[key] = {
            "role": roles[key], "part": part, "mode": mode, "weight": weight,
            "priority": scores[key], "depends_on": sorted(deps[key]),
            "adapter_ready": key in adapters,
            "application": f"{MODES[mode][0]} في «{info['ar']}» / {MODES[mode][1]} in '{info['en']}' — {reason}",
        }
    if set(items) != set(inventory) or sum(map(len, waves)) != len(inventory):
        raise ValueError("Incomplete catalog scheduling")
    part_summary = {
        pid: {"ar": part_info[pid]["ar"], "en": part_info[pid]["en"],
              "task_weight": task_weights.get(pid, 0),
              "assigned": sum(1 for k in inventory if part_of[k] == pid),
              "leads": leads[pid]}
        for pid in part_info}
    digest = hashlib.sha256(json.dumps(
        {k: [items[k]["part"], items[k]["mode"], items[k]["weight"]] for k in sorted(items)},
        ensure_ascii=False).encode("utf-8")).hexdigest()
    return {"schema": "kosif.black-dragon.brain.v2", "task": task,
            "total": len(inventory), "scheduled": len(inventory), "assigned": len(items),
            "selected_out": 0, "waves": waves,
            "roles": {stage: sum(roles[k] == stage for k in inventory) for stage in (*STAGES, "support")},
            "parts": part_summary,
            "modes": {m: sum(items[k]["mode"] == m for k in items) for m in MODES},
            "weights": {w: sum(items[k]["weight"] == w for k in items) for w in ("lead", "core", "support")},
            "assignment_sha256": digest,
            "items": items,
            "strategy": ("ALL items used: each gets a part, a mode and a weight; relevance orders "
                         "and weights but never removes; dependency-correct concurrent waves"),
            "limitations": ("Planning is lexical and deterministic, not an LLM; an assignment is not "
                            "execution and says nothing about artistic quality")}
