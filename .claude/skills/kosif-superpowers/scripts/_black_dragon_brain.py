#!/usr/bin/env python3
"""Deterministic planning brain for ALL Black Dragon catalog entries.

Uses text relevance to order work, never to omit a skill, power or tool.
Dependency layers are explicit; actual executions must be evidenced by runner.
This planner is not an LLM and cannot make a documentation card executable.
"""
from __future__ import annotations
import json
import re
from collections import defaultdict
from pathlib import Path

WORDS = re.compile(r"[\w\u0600-\u06ff]+", re.UNICODE)
STOP = {"and", "the", "for", "with", "from", "skill", "tool", "power",
        "من", "في", "على", "الى", "إلى", "مع", "كل", "عن", "ده", "هي"}
STAGES = {
    "analyze": ("think", "reason", "research", "inspect", "audit", "source", "تحليل", "بحث", "مراجعة", "تخطيط"),
    "build": ("render", "design", "edit", "montage", "animation", "video", "motion",
              "صمم", "ارسم", "مونتاج", "فيديو", "برمجة", "توليد", "إنشاء"),
    "verify": ("verify", "test", "check", "quality", "validation", "qa", "تحقق", "اختبار", "جودة"),
}

def tokens(text: str) -> set[str]:
    return {x.lower() for x in WORDS.findall(text) if len(x) > 1 and x.lower() not in STOP}

def metadata(index: dict, skill_root: Path) -> dict:
    """Optional registry descriptors for better rankings, not a filter."""
    result = {}
    paths = skill_root / "data" / "powers"
    for file in sorted(paths.glob("*.json")):
        try:
            obj = json.loads(file.read_text(encoding="utf-8"))
            rows = obj if isinstance(obj, list) else obj.get("powers", [])
            if not isinstance(rows, list):
                continue
            for row in rows:
                if not isinstance(row, dict) or not row.get("id"):
                    continue
                key = "power:" + str(row["id"])
                if key in index:
                    result[key] = " ".join(str(row.get(k, "")) for k in
                                           ("title", "ar", "en", "what", "how", "family", "domain", "tags"))
        except (ValueError, OSError):
            continue
    toolfile = skill_root / "data" / "tools.json"
    try:
        for row in json.loads(toolfile.read_text(encoding="utf-8")).get("tools", []):
            key = "tool:" + str(row.get("id", ""))
            if key in index:
                result[key] = " ".join(str(row.get(k, "")) for k in
                                       ("title_ar", "title_en", "summary_ar", "summary_en", "area", "keywords"))
    except (OSError, ValueError):
        pass
    return result

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

def plan(task: str, inventory: dict, adapters: dict, skill_root: Path | None = None) -> dict:
    if not task.strip():
        raise ValueError("Task cannot be empty")
    descriptions = metadata(inventory, skill_root) if skill_root is not None else {}
    task_words = tokens(task)
    deps = _validate_dependencies(inventory, adapters)
    scores, stages = {}, {}
    for key, meta in inventory.items():
        desc = " ".join((key, str(meta.get("source", "")), descriptions.get(key, "")))
        desc_words = tokens(desc)
        scores[key] = len(task_words & desc_words)
        stage_score = {stage: sum(1 for term in terms if term in desc.lower())
                       for stage, terms in STAGES.items()}
        stages[key] = max(STAGES, key=lambda s: (stage_score[s], -list(STAGES).index(s)))
        if not any(stage_score.values()):
            stages[key] = "support"
    # Kahn waves: no dependency may run until all of its prerequisites finished.
    remaining = {k: set(v) for k, v in deps.items()}
    waves = []
    done = set()
    while remaining:
        ready = [k for k, pending in remaining.items() if not pending]
        if not ready:
            raise ValueError("Cyclic Black Dragon adapter dependencies")
        ready.sort(key=lambda k: (-scores[k], k))
        waves.append(ready)
        done.update(ready)
        remaining = {k: pending - done for k, pending in remaining.items() if k not in done}
    items = {key: {"role": stages[key], "priority": scores[key], "depends_on": sorted(deps[key]),
                   "adapter_ready": key in adapters} for key in inventory}
    if set(items) != set(inventory) or sum(map(len, waves)) != len(inventory):
        raise ValueError("Incomplete catalog scheduling")
    return {"schema": "kosif.black-dragon.brain.v1", "task": task,
            "total": len(inventory), "scheduled": len(inventory),
            "selected_out": 0, "waves": waves, "roles": {
                stage: sum(stages[k] == stage for k in inventory)
                for stage in (*STAGES, "support")},
            "items": items,
            "strategy": "ALL items, relevance-prioritized; dependency-correct concurrent waves; no exclusions",
            "limitations": "Planning is heuristic; no proof of executing a capability or artistic quality"}
