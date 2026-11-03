#!/usr/bin/env python3
"""Independent native reasoning of التنين الأسود.

The controlled 26-faculty vocabulary and six-stage cycle were distilled from
Dragon Mind (_mind_vocab.py, main, source blob c716595cd0b7285610f67792ba28615c0802f0d5).
This is a local snapshot, NOT a runtime import, adapter, or executor.
The new grouping, method reconciliation and handoff logic below belongs to
the independent Black Dragon and never executes old source modules.
"""
from __future__ import annotations

import re
import unicodedata
from collections import defaultdict

# The six-step cognitive cycle the mind runs for every task.
CYCLE = [
    {"id": "frame", "ar": "أطّر المشكلة", "en": "Frame the problem"},
    {"id": "explore", "ar": "استكشف البدائل", "en": "Explore options"},
    {"id": "decide", "ar": "قرّر", "en": "Decide"},
    {"id": "build", "ar": "ابنِ", "en": "Build"},
    {"id": "verify", "ar": "تحقّق", "en": "Verify"},
    {"id": "learn", "ar": "تعلّم وسلّم", "en": "Learn and deliver"},
]

# id, Arabic name, cycle stage, input kinds, output kinds, keywords
FACULTIES = [
    ("perceive-media", "افحص الوسائط", "frame", ["video", "audio", "image"], ["data"],
     ["ffprobe", "inspect", "probe", "detect", "scene", "measure", "analy", "loudness meter",
      "فحص", "تحليل", "كشف", "قياس"]),
    ("transcribe", "فرّغ الكلام", "frame", ["audio", "video"], ["text"],
     ["transcri", "whisper", "speech-to-text", "subtitle", "caption", "words.json",
      "تفريغ", "ترجمة", "سبتايتل"]),
    ("research", "ابحث واجمع المصادر", "frame", ["text"], ["data"],
     ["research", "search", "discover", "source", "fetch", "download", "scrape", "crawl",
      "بحث", "مصادر", "تحميل"]),
    ("reason-plan", "فكّر وخطّط", "explore", ["text", "data"], ["plan"],
     ["plan", "think", "reason", "strategy", "decid", "brief", "council", "option",
      "تخطيط", "تفكير", "خطة", "قرار", "مجلس"]),
    ("write-story", "اكتب السيناريو والنص", "explore", ["plan"], ["text"],
     ["script", "story", "copy", "hook", "narrat", "headline", "سيناريو", "قصة", "نص", "هوك"]),
    ("design-visual", "صمّم بصريًا", "build", ["plan", "text"], ["image"],
     ["design", "layout", "typograph", "palette", "poster", "font", "brand", "thumbnail",
      "تصميم", "خط", "ألوان", "بوستر", "غلاف"]),
    ("arabic-type", "اكتب بالعربي صح", "build", ["text"], ["image"],
     ["arabic", "rtl", "kashida", "harakat", "bidi", "عربي", "عربية", "تشكيل"]),
    ("generate-image", "ولّد صورًا", "build", ["text", "image"], ["image"],
     ["generate image", "text-to-image", "image generation", "diffusion", "flux", "midjourney",
      "توليد صور", "صورة"]),
    ("generate-video", "ولّد فيديو", "build", ["text", "image"], ["video"],
     ["generate video", "text-to-video", "image-to-video", "kling", "veo", "sora", "seedance",
      "توليد فيديو"]),
    ("generate-audio", "ولّد صوتًا وموسيقى", "build", ["text"], ["audio"],
     ["tts", "voice", "music", "song", "suno", "speech synth", "صوت", "موسيقى", "أغنية", "تعليق صوتي"]),
    ("animate-motion", "حرّك (موشن)", "build", ["plan", "image", "text"], ["video"],
     ["animat", "motion", "kinetic", "keyframe", "easing", "tween", "gsap", "lottie", "remotion",
      "تحريك", "موشن", "انميشن"]),
    ("three-d", "ابنِ ثلاثي الأبعاد", "build", ["plan", "image"], ["video", "3d"],
     ["blender", "3d", "mesh", "glb", "three.js", "camera orbit", "ثلاثي"]),
    ("edit-video", "اقطع ومنتج", "build", ["video", "audio"], ["video"],
     ["montage", "edit", "cut", "trim", "silence", "b-roll", "broll", "timeline", "reel", "video",
      "مونتاج", "قص", "ريلز", "فيديو"]),
    ("color-grade", "لوّن الصورة", "build", ["video", "image"], ["video", "image"],
     ["color", "colour", "grade", "lut", "tone", "bt.709", "تلوين", "لون"]),
    ("audio-mix", "امزج الصوت", "build", ["audio"], ["audio"],
     ["mix", "lufs", "duck", "beat", "bpm", "sync", "loudnorm", "مزج", "إيقاع", "مزامنة"]),
    ("render-encode", "ارندر وصدّر", "build", ["video", "plan"], ["video"],
     ["render", "encode", "ffmpeg", "export", "h.264", "x264", "mp4", "crf", "رندر", "تصدير"]),
    ("web-build", "ابنِ صفحات ومواقع", "build", ["plan", "text"], ["web"],
     ["html", "css", "website", "web page", "react", "site", "landing", "موقع", "صفحة"]),
    ("code-engineering", "برمج وهندس", "build", ["plan", "code"], ["code"],
     ["code", "refactor", "api", "python", "javascript", "library", "cli", "repository",
      "برمجة", "كود"]),
    ("data-analysis", "حلّل البيانات", "explore", ["data"], ["data"],
     ["dataset", "chart", "csv", "statistic", "metric", "dashboard", "graph", "بيانات", "إحصاء"]),
    ("verify-qa", "تحقّق واختبر", "verify", ["video", "audio", "image", "code", "web", "data"], ["receipt"],
     ["verify", "test", "check", "qa", "validat", "lint", "audit", "receipt", "proof", "gate",
      "تحقق", "اختبار", "جودة", "إيصال"]),
    ("safety-rights", "احمِ الحقوق والأمان", "verify", ["data", "text"], ["receipt"],
     ["rights", "licen", "privacy", "secret", "permission", "consent", "safety", "guard",
      "حقوق", "ترخيص", "خصوصية", "أمان"]),
    ("deliver-publish", "سلّم وانشر", "learn", ["video", "web", "code", "text"], ["delivery"],
     ["deliver", "publish", "upload", "share", "deploy", "package", "zip", "tiktok", "instagram",
      "youtube", "تسليم", "نشر", "رفع", "تيك توك", "انستجرام", "يوتيوب"]),
    ("memory-learn", "تذكّر وتعلّم", "learn", ["receipt", "data"], ["data"],
     ["memory", "recipe", "lesson", "learn", "ledger", "fusionforge", "remember", "ذاكرة", "درس", "تعلم"]),
    ("orchestrate", "نسّق الوكلاء", "decide", ["plan"], ["plan"],
     ["orchestr", "agent", "parallel", "pipeline", "workflow", "dispatch", "subagent",
      "تنسيق", "وكلاء", "توازي"]),
    ("protocol-govern", "التزم بالبروتوكول", "decide", ["plan"], ["plan"],
     ["protocol", "usip", "rule", "policy", "standard", "appendix", "بروتوكول", "قاعدة"]),
    ("visual-reference", "استلهم مرجعًا بصريًا", "explore", ["text"], ["plan"],
     ["style", "reference", "look", "aesthetic", "inspiration", "promptsmotion", "مرجع", "ستايل"]),
]


FACULTY_IDS = [row[0] for row in FACULTIES]
FACULTY = {row[0]: {"ar": row[1], "stage": row[2], "inputs": row[3],
                    "outputs": row[4], "keywords": row[5]} for row in FACULTIES}
STAGES = [stage["id"] for stage in CYCLE]
FALLBACK = {"tool": "code-engineering", "protocol": "protocol-govern",
            "playbook": "protocol-govern", "style": "visual-reference"}
ALWAYS = ("reason-plan", "verify-qa", "safety-rights", "deliver-publish", "memory-learn")
FRAMEWORK = {
    "frame": ("first-principles", "What is required and what is assumed?",
              "Task scope and inputs are explicit."),
    "explore": ("scamper", "Which methods complement each other without losing constraints?",
                "Distinct source ideas remain traceable."),
    "decide": ("expected-value", "Which combination covers the task with the fewest unsupported assumptions?",
               "Missing dependencies and consent needs are named."),
    "build": ("mvp", "What smallest actual output would demonstrate the method?",
              "Do not claim a completed artifact without an execution receipt."),
    "verify": ("pre-mortem", "How might the output fail or violate user constraints?",
               "Functional evidence must be checked separately from source links."),
    "learn": ("after-action-review", "Which proven details should become reusable?",
              "Original IDs and hashes are retained.")
}


def _normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", str(text)).lower()
    return re.sub(r"\s+", " ", text).strip()


def _keyword_match(text: str, keyword: str) -> bool:
    keyword = _normalize(keyword)
    if not keyword:
        return False
    if re.match(r"[a-z0-9]", keyword):
        return re.search(r"(?<![a-z0-9])" + re.escape(keyword), text) is not None
    return keyword in text


def classify(item: dict) -> list[dict]:
    """Map an actual extracted catalog entry to up to four mental faculties."""
    body = _normalize(" ".join(str(item.get(k, "")) for k in
                               ("id", "title", "purpose", "method", "faculty")))
    scores = {}
    for fid in FACULTY_IDS:
        score = sum(1 for stem in FACULTY[fid]["keywords"] if _keyword_match(body, stem))
        if score:
            scores[fid] = score
    if not scores:
        scores[FALLBACK.get(item.get("kind"), "reason-plan")] = 0
    ranking = sorted(scores, key=lambda fid: (-scores[fid], FACULTY_IDS.index(fid)))
    return [{"faculty": fid, "score": scores[fid],
             "stage": FACULTY[fid]["stage"]} for fid in ranking[:4]]


def _method_fragments(item: dict) -> list[str]:
    """Preserve distinct instructions; no unsafe fuzzy deletion of constraints."""
    raw = str(item.get("method") or item.get("purpose") or item.get("title") or "")
    fragments = re.split(r"[;\n]+", raw)
    parts = [re.sub(r"\s+", " ", x).strip() for x in fragments if x.strip()]
    # A source's text may be long. Keep original fingerprints for full detail.
    return parts[:32] or [str(item.get("title") or item.get("id"))]


def fuse(task: str, selected: list[dict], catalog_total: int) -> dict:
    """Synthesize a new, evidence-linked cognitive recipe without running old tools.

    Exact duplicate instructions are coalesced *within the same faculty* while
    accumulating every contributing source ID. Similar but non-identical ideas
    are kept intact so that exceptions and constraints cannot be discarded.
    """
    if not isinstance(task, str) or not task.strip():
        raise ValueError("task cannot be empty")
    task_faculties = classify({"kind": "skill", "title": task})
    grouped = defaultdict(lambda: {"sources": set(), "methods": {}})
    affiliation = []
    raw_method_count = 0

    for item in selected:
        sid = item["id"]
        facets = classify(item)
        affiliation.append({"source_id": sid, "faculties": [f["faculty"] for f in facets]})
        primary = facets[0]["faculty"]
        group = grouped[primary]
        group["sources"].add(sid)
        for step in _method_fragments(item):
            raw_method_count += 1
            normalized = _normalize(step)
            if normalized not in group["methods"]:
                group["methods"][normalized] = {"method": step[:1200], "source_ids": []}
            if sid not in group["methods"][normalized]["source_ids"]:
                group["methods"][normalized]["source_ids"].append(sid)

    # The always-on thinking disciplines are native *rules*, not retroactively
    # claimed as extracted capabilities or executed source tools.
    involved = set(grouped) | {f["faculty"] for f in task_faculties} | set(ALWAYS)
    faculties = []
    for fid in sorted(involved, key=lambda x: (STAGES.index(FACULTY[x]["stage"]), FACULTY_IDS.index(x))):
        info = FACULTY[fid]
        members = grouped.get(fid)
        methods = [] if not members else list(members["methods"].values())
        methods.sort(key=lambda x: (_normalize(x["method"]), x["source_ids"]))
        faculties.append({
            "faculty": fid, "name_ar": info["ar"], "stage": info["stage"],
            "inputs": info["inputs"], "outputs": info["outputs"],
            "source_ids": sorted(members["sources"]) if members else [],
            "merged_methods": methods,
            "role": "extracted-from-selected-sources" if members else "native-thinking-discipline",
            "implementation": "reasoning-recipe-not-media-or-tool-execution"
        })

    # Typed handoff checks are generated in the new engine, no Dragon Mind call.
    produced = {"text": "task"}
    handoffs, gaps = [], []
    for group in faculties:
        matches = [(k, produced[k]) for k in group["inputs"] if k in produced]
        src = matches[0][1] if matches else None
        handoffs.append({"from": src or "external-input-required", "to": group["faculty"],
                         "media": matches[0][0] if matches else None})
        if not matches and group["source_ids"]:
            gaps.append({"faculty": group["faculty"], "kind": "missing-typed-input",
                         "requires_any": group["inputs"]})
        for kind in group["outputs"]:
            produced[kind] = group["faculty"]

    cycle = []
    for stage in CYCLE:
        fid = [f for f in faculties if f["stage"] == stage["id"]]
        fw, question, check = FRAMEWORK[stage["id"]]
        cycle.append({"stage": stage["id"], "name_ar": stage["ar"],
                      "reasoning_method": fw, "question": question, "check": check,
                      "faculties": [f["faculty"] for f in fid],
                      "source_ids": sorted({sid for f in fid for sid in f["source_ids"]})})

    return {
        "engine": "black-dragon-independent-native-mind",
        "source_inspiration": "Dragon Mind 26-faculty taxonomy and six-stage cycle",
        "runtime_legacy_imports": False,
        "catalog_total": catalog_total,
        "selected_source_count": len(selected),
        "faculties": faculties,
        "affiliation": affiliation,
        "cognitive_cycle": cycle,
        "typed_handoffs": handoffs,
        "critic": gaps + [{"kind": "execution-not-proven",
                           "detail": "Native reasoning and provenance are not proof of executing media, APIs or every catalog ability."}],
        "method_fusion": {"source_fragments": raw_method_count,
                          "distinct_fragments": sum(len(f["merged_methods"]) for f in faculties),
                          "deduplicated_exact_fragments": raw_method_count -
                          sum(len(f["merged_methods"]) for f in faculties)},
        "provenance_preserved": sorted({s["id"] for s in selected}) ==
                                sorted({x["source_id"] for x in affiliation}),
        "status": "native-reasoning-implemented; original-capabilities-not-all-reimplemented"
    }
