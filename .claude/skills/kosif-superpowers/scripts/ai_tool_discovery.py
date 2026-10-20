#!/usr/bin/env python3
"""KOSIF local task-to-capability matching, independent of commercial directory code.

The source is KOSIF's OWN capability_atlas_index.json. No requests to external
sites, no hidden APIs, and no claim to implement another site's search ranking.
"""
import argparse
from collections import Counter
import json
import math
from pathlib import Path
import re
import unicodedata

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "data" / "capability_atlas_index.json"
STOP = {"a", "an", "the", "for", "and", "with", "to", "of", "in", "do", "i",
        "my", "need", "want", "please", "عايز", "اريد", "انا", "الي", "اللي",
        "من", "في", "على", "عن", "مع", "عمل", "اعمل", "ممكن"}
ALIAS = {
    "رسم": ("draw", "painting", "illustration", "sketch", "vector"),
    "ارسم": ("draw", "painting", "sketch"),
    "فيديو": ("video", "render", "motion"),
    "تحريك": ("animation", "motion", "rig", "keyframe"),
    "صوره": ("image", "photo", "picture"),
    "صور": ("image", "photo", "picture"),
    "مونتاج": ("video", "editing", "cuts", "compositing"),
    "موسيقى": ("music", "beat", "audio"),
    "شخصيات": ("character", "rig", "skeleton"),
    "ثلاثي": ("3d", "geometry", "scene"),
    "ابحث": ("search", "discovery", "research"),
    "البحث": ("search", "discovery", "research"),
    "ادوات": ("tools", "capability", "discovery"),
}
FIELDS = (("name_en", 6.0), ("name_ar", 6.0), ("tags", 4.0),
          ("when", 2.0), ("summary", 1.0))


def normalize(text):
    if not isinstance(text, str):
        return ""
    text = unicodedata.normalize("NFKC", text).casefold()
    text = re.sub(r"[\u064b-\u065f\u0670]", "", text)
    text = text.translate(str.maketrans({"أ":"ا","إ":"ا","آ":"ا","ى":"ي","ة":"ه","ـ":""}))
    return text


def terms(text):
    return [t for t in re.findall(r"[^\W_]+", normalize(text), flags=re.UNICODE)
            if len(t) > 1 and t not in STOP]


def intent_tokens(task):
    explicit = terms(task)
    if not explicit:
        raise ValueError("query must contain useful task words")
    expanded = set(explicit)
    for term in explicit:
        expanded.update(ALIAS.get(term, ()))
    return explicit, expanded


def load_index(index=INDEX):
    data = json.loads(Path(index).read_text(encoding="utf-8-sig"))
    records = data["powers"]
    if not isinstance(records, list) or not records:
        raise ValueError("missing KOSIF capabilities")
    if len({r["id"] for r in records}) != len(records):
        raise ValueError("duplicate capability IDs")
    return records


def rank(task, records, limit=8):
    if type(limit) is not int or not (1 <= limit <= 30):
        raise ValueError("limit must be 1-30")
    explicit, expanded = intent_tokens(task)
    # Corpus-relative inverse frequency: common vague words get less weight.
    docs = []
    df = Counter()
    for row in records:
        blobs = {}
        merged = set()
        for field, weight in FIELDS:
            value = row.get(field, "")
            if isinstance(value, list):
                value = " ".join(str(x) for x in value)
            tok = set(terms(str(value)))
            blobs[field] = tok
            merged.update(tok)
        df.update(merged)
        docs.append((row, blobs))
    length = len(records)
    matches = []
    for row, blobs in docs:
        contributions = {}
        matched_explicit = 0
        for term in expanded:
            w = math.log(1 + (length + 1)/(df[term] + 1))
            if term in explicit:
                w *= 1.3
            score = sum(weight for field, weight in FIELDS if term in blobs[field])
            if score:
                contributions[term] = round(w*score, 4)
                if term in explicit:
                    matched_explicit += 1
        if not contributions:
            continue
        score = sum(contributions.values())
        score *= 0.55 + 0.45*matched_explicit/len(set(explicit))
        # Status is descriptive metadata, NOT a runtime pass indicator.
        matches.append({"id": row["id"],
                        "name": row.get("name_en") or row.get("name_ar"),
                        "name_ar": row.get("name_ar"),
                        "score": round(score, 3),
                        "matched_terms": sorted(contributions, key=lambda k:-contributions[k])[:8],
                        "claimed_catalog_status": row.get("status"),
                        "proof_scope": row.get("proof_scope"),
                        "requirements": row.get("requires", []),
                        "runtime_verified": False,
                        "source": row.get("source")})
    matches.sort(key=lambda r: (-r["score"], r["id"]))
    return {"schema":"kosif.original-discovery.v1", "task":task,
            "catalog_size":len(records), "external_requests":0,
            "algorithm":"original weighted token match + corpus rarity + coverage",
            "claim":"Ranking is local candidate discovery only; no third-party search algorithm copied.",
            "results":matches[:limit]}


def main():
    p = argparse.ArgumentParser(description="KOSIF offline bilingual capability finder")
    p.add_argument("task", nargs="?")
    p.add_argument("--top", type=int, default=8)
    p.add_argument("--doctor", action="store_true")
    args = p.parse_args()
    records = load_index()
    if args.doctor:
        out = {"status":"index_available", "records":len(records),
               "network_requests":0, "features":["bilingual", "local-index", "requirements", "evidence-labels"]}
    elif args.task:
        try:
            out = rank(args.task, records, args.top)
        except ValueError as exc:  # e.g. a stop-word-only task or --top out of range
            p.error(str(exc))
    else:
        p.error("task or --doctor required")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
