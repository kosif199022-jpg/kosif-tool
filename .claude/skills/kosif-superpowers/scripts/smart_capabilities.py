#!/usr/bin/env python3
"""Deterministic full-coverage superpowers index, group router and Claude 3-minute digest.

Run from any directory:
  python scripts/smart_capabilities.py build
  python scripts/smart_capabilities.py verify
  python scripts/smart_capabilities.py groups
  python scripts/smart_capabilities.py find "رسم خطوط وأشكال" --json

Catalog classification is an information architecture, NOT proof that separate
runtimes were technically merged or reverse-engineered.
"""
from __future__ import annotations
import argparse
import collections
import json
import re
import sys
from datetime import date
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
POWERS = BASE / "data" / "powers"
OUT = BASE / "data" / "smart_capability_index.json"
DOC = BASE / "references" / "SMART_CAPABILITY_GROUPS.md"
QUICK = BASE / "references" / "CLAUDE_3_MINUTE_MAP.md"
MANIFEST = BASE / "manifest.json"

# Every existing capability keeps its original ID, status, proof and requirements.
# Integration candidates are logical workflows, not assertions of tested interoperability.
SPEC = [
 ("research", "البحث والمعرفة", "Research & knowledge",
  "atlas-research,web-research,knowledge-graph",
  "research web source citations evidence knowledge search بحث مصادر مراجع معرفة"),
 ("thinking", "التفكير والتخطيط والاستراتيجية", "Reasoning & strategy",
  "atlas-mind,atlas-strategy,creativity-engine,mental-models,planning-execution,prompt-craft,strategy-finance,thinking-core",
  "think reasoning idea brainstorm strategy plan finance decision تحليل تخطيط ابتكار قرار"),
 ("agents", "الوكلاء والتوجيه الذكي", "Agents & routing",
  "agent-orchestration,runnable-tools,self-discovery",
  "agent orchestration tool routing discover automation وكلاء أدوات توجيه بحث"),
 ("software", "البرمجة وبناء التطبيقات", "Software & applications",
  "app-feature-transfer,apps-artifacts,atlas-build,atlas-code,code-engineering,ui-product-device",
  "code programming apps api software frontend backend ui تطبيق برمجة واجهات تطوير"),
 ("drawing", "الرسم والأشكال والتصميم", "Drawing & visual composition",
  "brand-logo-identity,diagrams-explainers-code,hand-drawn-draw-on,pixel-retro-stylized,shapes-morph-geometry",
  "draw line stroke path shape circle polygon vector svg logo illustration diagram رسم خطوط أشكال دائرة مضلع شعار مخطط"),
 ("images", "الصور والتحرير والتوليد", "Images & photo editing",
  "ai-generation,atlas-media,color-palette-grading,media-image-audio,photo-video-footage",
  "image photo photoshop paint color grading generate edit صور تعديل تلوين فوتوشوب توليد"),
 ("3d", "الثري دي والمحاكاة والرندر", "3D & rendering",
  "3d-spatial,engines-render-pipeline,light-glow-bloom,particles-fluids-physics,texture-material",
  "blender 3d model mesh material texture light render cycles simulation ثري دي بلندر رندر خامة إضاءة"),
 ("motion", "الموشن والمونتاج والسينما", "Motion & video editing",
  "camera-composition-layout,characters-rigs,easing-timing-rhythm,formats-platforms,story-direction-ideas,transitions-cuts,video-download",
  "video film montage edit scene camera animation cut transition character motion فيديو مونتاج تحريك كاميرا مشهد انتقالات"),
 ("audio", "الصوت والموسيقى والتعليق", "Audio & voice",
  "audio-sync-captions,music-beat-sound,voice-tts",
  "audio music voice speech tts subtitles beat sync caption صوت موسيقى تعليق ترجمة توقيت"),
 ("type", "الخطوط والنصوص العربية واللاتينية", "Typography & localization",
  "arabic-language,typography-arabic,typography-latin",
  "arabic text typography font subtitle rtl letter line خط خطوط عربي كتابة تنسيق نص"),
 ("data", "البيانات والرسوم والمواقع", "Data & visual analytics",
  "atlas-data,charts-data-infographic,data-analysis,maps-geo",
  "data chart dashboard graph excel map gis analytics بيانات إكسل رسوم مخطط خرائط"),
 ("documents", "المستندات والكتابة", "Documents & writing",
  "atlas-craft,atlas-docs,documents-office,writing-humanizer",
  "document pdf word excel office writing report مستند تقرير كتابة وورد"),
 ("quality", "الاختبارات والجودة والأمان", "QA & security",
  "api-testing,qa-verification,security-safety,verification-evals",
  "test verify validation audit qa security eval اختبار مراجعة توثيق أمان"),
 ("reverse", "التحليل العكسي وفحص البرامج", "Reverse engineering",
  "software-investigation",
  "reverse engineering ghidra rea binary executable forensic تحليل عكسي جفرا ريش"),
 ("misc", "قدرات مساندة غير مصنفة", "Other supporting capabilities",
  "other",
  "other legacy مساعد إضافي متنوع"),
]
WORKFLOWS = {
 "drawing": ["الخطوط والمسارات", "الأشكال والهندسة", "الدمج في مشهد/لوحة", "التصدير والتحقق"],
 "images": ["استيراد الصورة", "التحرير والتلوين", "التوليد الاختياري", "تصدير النتيجة"],
 "3d": ["إنشاء/استيراد المجسم", "الخامات والإضاءة", "المحاكاة/التحريك", "الرندر والتحقق"],
 "motion": ["القصة والستوريبورد", "التوقيت والكاميرا", "التحريك والمونتاج", "التصدير"],
 "audio": ["المعالجة", "المزامنة", "التعليق والترجمة", "التحقق"],
 "data": ["الاستيراد والتنظيف", "التحليل", "الرسم والخرائط", "التصدير"],
 "software": ["التصميم", "البرمجة", "الاختبار", "النشر"],
 "quality": ["الجرد", "التقييم", "اختبارات الانحدار", "إثبات النتائج"],
}

def words(s):
    return set(re.findall(r"[\w]+", str(s or "").casefold(), re.UNICODE))

def load():
    specs = {}
    families = {}
    for slug, ar, en, csv, keys in SPEC:
        fs = [x.strip() for x in csv.split(",")]
        specs[slug] = {"id": slug, "ar": ar, "en": en, "families": fs,
                       "keywords": keys, "workflow": WORKFLOWS.get(slug, [])}
        for f in fs:
            if f in families:
                raise ValueError("Double-classified family: " + f)
            families[f] = slug
    records = []
    for filename in sorted(POWERS.glob("*.json")):
        source = json.loads(filename.read_text(encoding="utf-8-sig"))
        if not isinstance(source, list):
            raise ValueError("Expected list: " + str(filename))
        for entry in source:
            family = entry.get("family")
            if family not in families:
                raise ValueError("Unclassified family: " + str(family))
            records.append({
              "id": entry["id"], "family": family, "group": families[family],
              "domain": entry.get("domain",""),
              "name_en": entry.get("name_en",""),
              "name_ar": entry.get("name_ar",""),
              "status": entry.get("status",""),
              "requires": entry.get("requires",[]),
              "proof": entry.get("proof",[]),
              "source": filename.name,
              "what": str(entry.get("what",""))[:280]
            })
    ids = [x["id"] for x in records]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate power IDs: " + str([x for x,c in collections.Counter(ids).items() if c > 1][:10]))
    actual = {x["family"] for x in records}
    missing = set(families)-actual
    if missing:
        raise ValueError("Families without powers: " + repr(sorted(missing)))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8-sig"))
    expected = manifest["counts"]["powers"]
    if expected != len(records):
        raise ValueError(f"Manifest mismatch: {expected} vs {len(records)}")
    counts = collections.Counter(x["group"] for x in records)
    for slug, g in specs.items():
        gr = [x for x in records if x["group"] == slug]
        g["count"] = counts[slug]
        g["status_counts"] = dict(sorted(collections.Counter(x["status"] for x in gr).items()))
        g["family_counts"] = dict(sorted(collections.Counter(x["family"] for x in gr).items()))
        gr.sort(key=lambda x: ({"proven":0,"ready":1,"documented":2,"seen":3,"install":4,"key":5,"idea":6}.get(x["status"], 7),x["id"]))
        g["examples"] = [{"id":x["id"],"title":x["name_en"],"status":x["status"]} for x in gr[:5]]
    return {"schema":"kosif.smart-capability-index.v1",
            "origin":"data/powers/*.json (catalog); no original records changed",
            "catalog_powers":len(records),"group_count":len(specs),
            "family_count":len(actual),"tool_count":manifest["counts"]["tools"],
            "groups":list(specs.values()),"powers":records,
            "notes":["Logical grouping only; integration and binary validation are separate steps.",
                     "Power status and source evidence retained; never infer availability from membership."]}

def save(index):
    OUT.write_text(json.dumps(index,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    lines = ["# KOSIF unified capability groups",
             "",f"Source: {index['catalog_powers']:,} powers / {index['family_count']} families / {index['group_count']} integrated-domain candidates.",
             "","> These are navigation/integration **candidates**, not evidence that all tools were merged into one runtime.",
             "", "| Group | Arabic | Powers | Families |",
             "|---|---|---:|---:|"]
    for g in index["groups"]:
        lines.append(f"| `{g['id']}` | {g['ar']} | {g['count']:,} | {len(g['families'])} |")
    lines += ["", "## Integration approach", "",
              "Keep all original IDs, statuses, requirements and proofs. Use a common entrypoint per group while testing actual component interoperability. No deletion of originals before regression tests.",
              "", "## Workflows (design targets, not yet tested)", ""]
    for g in index["groups"]:
        if g["workflow"]:
            lines += [f"### {g['ar']} (`{g['id']}`)", " → ".join(g["workflow"]), ""]
    DOC.write_text("\n".join(lines)+"\n",encoding="utf-8")
    quick = [
      "# Claude: understand KOSIF in under three minutes",
      "", "## 30-second map",
      f"Full catalog: {index['catalog_powers']:,} power records, {index['family_count']} families, {index['group_count']} groups; {index['tool_count']} tool records in existing manifest.",
      "Classification is NOT proof of runtime compatibility. Respect each power's status, requirements, proof.",
      "", "## Commands (run from .claude/skills/kosif-superpowers)",
      "```sh",
      "python scripts/smart_capabilities.py groups",
      'python scripts/smart_capabilities.py find "رسم خطوط وأشكال" --json',
      'python scripts/hub.py find "<user task>" --json',
      "python scripts/hub.py doctor --json",
      "python scripts/smart_capabilities.py verify",
      "```", "", "## Group routing cheatsheet", ""
    ]
    for g in index["groups"]:
        quick.append(f"- **{g['ar']}** (`{g['id']}`, {g['count']:,}): "+", ".join(g["families"]))
    quick += ["","## Work without losing provenance","",
              "1. Route user task to a group using smart_capabilities.py find.",
              "2. Inspect specific power IDs and actual tool cards with hub.py.",
              "3. Check present requirements using hub.py doctor.",
              "4. Use REA for legitimate source/metadata-assisted inspections, Ghidra for authorized binaries only.",
              "5. Do not claim modules are interoperable until an end-to-end test passes.",
              "6. Document executable pipelines with inputs, outputs, error handling and proofs."]
    QUICK.write_text("\n".join(quick)+"\n",encoding="utf-8")

def find(index, query, limit=5):
    q = words(query)
    scores = []
    for g in index["groups"]:
        groupwords = words(" ".join([g["ar"], g["en"], g["keywords"], " ".join(g["families"])]))
        base = len(q & groupwords)*7
        ranked = []
        for power in index["powers"]:
            if power["group"] != g["id"]:
                continue
            title_words = words(power["name_ar"]+" "+power["name_en"])
            descr_words = words(power["what"])
            hit = len(q & title_words)*5 + len(q & descr_words)
            if hit:
                ranked.append((hit, power))
        ranked.sort(key=lambda p:(-p[0],p[1]["id"]))
        score = base + sum(x[0] for x in ranked[:4])
        if score:
            scores.append({"group":g["id"],"name":g["ar"],"score":score,
                           "total":g["count"],"candidate_powers":[{"id":p["id"],"name":p["name_en"],"status":p["status"],"requires":p["requires"]} for _,p in ranked[:6]],
                           "workflow":g["workflow"]})
    return sorted(scores,key=lambda s:(-s["score"],s["group"]))[:limit]

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("action",choices=("build","verify","groups","find"))
    p.add_argument("query",nargs="?",default="")
    p.add_argument("--json",action="store_true")
    p.add_argument("--limit",type=int,default=5)
    a=p.parse_args()
    idx=load()
    if a.action=="build":
        save(idx)
        out={"built":str(OUT),"doc":str(DOC),"quick":str(QUICK),
             "powers":idx["catalog_powers"],"groups":idx["group_count"],"families":idx["family_count"]}
    elif a.action=="verify":
        disk=json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
        keys=("powers","groups","catalog_powers","family_count","group_count","tool_count")
        stale=[k for k in keys if disk.get(k)!=idx[k]]
        out={"pass":not stale,"stale":stale,
             "powers":len(idx["powers"]),"groups":idx["group_count"],
             "families":idx["family_count"],"tools":idx["tool_count"]}
        if not out["pass"]: sys.exit("Smart index is stale ("+", ".join(stale)+"); run build.")
    elif a.action=="groups":
        out=[{"group":g["id"],"ar":g["ar"],"powers":g["count"],
              "families":len(g["families"]),"status_counts":g["status_counts"]} for g in idx["groups"]]
    else:
        if not a.query: p.error("find needs a search query")
        out=find(idx,a.query,a.limit)
    print(json.dumps(out,ensure_ascii=False,indent=2) if a.json or a.action!="groups" else
      "\n".join(f"{g['group']:12} {g['powers']:5} | {g['ar']}" for g in out))
if __name__=="__main__": main()
