#!/usr/bin/env python3
"""KOSIF Universal Skill Intelligence Protocol — محرك بروتوكول ذكاء المهارات الشامل.

The machine half of PROTOCOL.md. For any request it:
  0. checks the environment and that every derived index is fresh,
  1. writes a structured request analysis (intents, deliverable, constraints, files, open questions),
  2. scans 100% of the catalog records (every data/powers/*.json row) and returns a coverage receipt that fails
     closed when any record is unreadable, unclassified or missing from a group,
  3. ranks groups, fused superpowers, powers and runnable tools; adds complements, verifiers and cross-domain picks,
  4. scores candidates (fit 35 · integration 20 · feasibility 15 · evidence 10 · cost 10 · creativity 10),
  5. drafts plans A (smart & fast) · B (professional & balanced) · C (maximum & inventive) with counts, tools,
     requirements present/missing, risks and a recommendation, and the approval question.

  python3 skill_intelligence.py brief "<request in the user's words>" [--json] [--out FILE] [--details]
  python3 skill_intelligence.py verify          # coverage + freshness only (exit 1 on any gap)

It never executes a catalog capability, installs anything or contacts the network. The plans are a draft for
Claude to think over, improve and present; the user's one-word answer decides what runs.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import math
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
REPO = SKILL.parents[2] if len(SKILL.parents) >= 3 else SKILL
sys.path.insert(0, str(HERE))
import powers as P  # noqa: E402

POWERS = SKILL / "data" / "powers"
SMART = SKILL / "data" / "smart_capability_index.json"
SP = SKILL / "data" / "superpowers.json"
TOOLS = SKILL / "data" / "tools.json"
MIND = SKILL / "data" / "capability_mindmap.json"
WEIGHTS = {"fit": 35, "integration": 20, "feasibility": 15, "evidence": 10, "cost": 10, "creativity": 10}
EVIDENCE = {"proven": 1.0, "ready": 0.85, "install": 0.6, "key": 0.45, "seen": 0.4, "documented": 0.3, "idea": 0.1}
STAGE_ORDER = ["understand", "plan", "create", "refine", "assemble", "verify", "deliver"]
STOP = set(("the and for with from that this your make build want need what how please a an is are of to my can i you me it in on "
            "عايز اعمل عمل من في على عن الى إلى و ال دي ده دول هذا هذه لي هل ممكن اريد أريد ابغى ابي عاوز يا مع كل بعد قبل").split())
MAX_HINTS = ("أقصى", "اقصى", "احترافي جدا", "بأقصى", "كل القدرات", "maximum", "max", "ultimate", "best possible", "cinematic", "سينمائي")
FAST_HINTS = ("بسرعة", "سريع", "مختصر", "quick", "fast", "simple", "بسيط", "سطر", "one line")


# ------------------------------------------------------------------ helpers
def jload(p: Path, default=None):
    try:
        return json.loads(p.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        return default


def norm_ar(s: str) -> str:
    s = re.sub(r"[ً-ْـ]", "", s or "")
    return s.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا").replace("ة", "ه").replace("ى", "ي")


def tokens(s: str) -> list:
    s = norm_ar(str(s or "").lower())
    return [w for w in re.findall(r"[a-z0-9][a-z0-9+#.-]+|[؀-ۿ]{2,}", s) if w not in STOP]


def expand(query: str) -> list:
    """Query words + Arabic→English bridges (atlas miner aliases + powers.py intent words) + light Arabic stemming."""
    words = tokens(query)
    out = list(words)
    try:
        import atlas_capability_miner as AM
        out += AM.expand_query(query)
    except Exception:  # noqa: BLE001
        pass
    for w in words:
        if re.match(r"[؀-ۿ]", w):
            for pre in ("وال", "بال", "لل", "ال", "و", "ب", "ل", "ف"):
                if w.startswith(pre) and len(w) - len(pre) >= 3:
                    out.append(w[len(pre):])
                    break
    return list(dict.fromkeys(x for x in out if x and x not in STOP))


def sha_catalog():
    h = hashlib.sha256()
    files = sorted(POWERS.glob("*.json"))
    for f in files:
        h.update(f.name.encode())
        h.update(f.read_bytes())
    return h.hexdigest(), len(files)


# ------------------------------------------------------------------ stage 0: environment & freshness
def environment() -> dict:
    env = {"python": sys.version.split()[0], "tools": {}}
    for b in ("ffmpeg", "ffprobe", "node", "git", "rea", "blender", "yt-dlp"):
        env["tools"][b] = bool(shutil.which(b))
    try:
        r = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True, timeout=10)
        env["git_branch"] = r.stdout.strip() or None
        r = subprocess.run(["git", "-C", str(REPO), "status", "--porcelain"], capture_output=True, text=True, timeout=20)
        env["git_dirty_files"] = len([l for l in r.stdout.splitlines() if l.strip()])
    except (OSError, subprocess.TimeoutExpired):
        env["git_branch"] = None
    return env


def tool_readiness() -> dict:
    try:
        r = subprocess.run([sys.executable, str(HERE / "hub.py"), "doctor", "--json"], capture_output=True, text=True, timeout=120)
        d = json.loads(r.stdout)
        return {"summary": d.get("summary", {}), "state": {t["id"]: t.get("state") for t in d.get("tools", [])}}
    except Exception as exc:  # noqa: BLE001
        return {"summary": {"error": str(exc)[:200]}, "state": {}}


# ------------------------------------------------------------------ stage 2: full coverage scan
def scan_catalog() -> dict:
    """Read every record of every data/powers/*.json; classify each into its group; fail closed on any gap."""
    import smart_capabilities as SC
    fam2group = {}
    for slug, _ar, _en, csv, _k in SC.SPEC:
        for f in csv.split(","):
            fam2group[f.strip()] = slug
    records, broken, unclassified = [], [], []
    for f in sorted(POWERS.glob("*.json")):
        try:
            rows = json.loads(f.read_text(encoding="utf-8-sig"))
            if not isinstance(rows, list):
                raise ValueError("not a list")
        except (OSError, ValueError) as exc:
            broken.append({"file": f.name, "error": str(exc)[:160]})
            continue
        for i, r in enumerate(rows):
            if not isinstance(r, dict) or not r.get("id"):
                broken.append({"file": f.name, "row": i, "error": "record without id"})
                continue
            g = fam2group.get(r.get("family"))
            if not g:
                unclassified.append(r.get("id"))
            records.append({"id": r["id"], "family": r.get("family"), "group": g, "domain": r.get("domain") or "motion",
                            "status": r.get("status"), "name_en": r.get("name_en", ""), "name_ar": r.get("name_ar", ""),
                            "requires": r.get("requires") or [], "section": r.get("section", ""),
                            "text": " ".join([str(r.get("name_en", "")), str(r.get("name_ar", "")), " ".join(map(str, r.get("tags") or [])),
                                              str(r.get("section", "")), str(r.get("when", "")), str(r.get("what", ""))[:400]]),
                            "file": f.name})
    ids = [r["id"] for r in records]
    dup = [k for k, v in collections.Counter(ids).items() if v > 1]
    digest, nfiles = sha_catalog()
    groups = collections.Counter(r["group"] for r in records if r["group"])
    families = {r["family"] for r in records}
    receipt = {"catalog_sha256": digest, "files": nfiles, "records_on_disk": len(records), "records_scanned": len(records),
               "records_classified": sum(1 for r in records if r["group"]), "unclassified": unclassified[:20], "unclassified_count": len(unclassified),
               "broken": broken[:20], "broken_count": len(broken), "duplicate_ids": dup[:20], "families": len(families),
               "groups": len(groups), "group_sizes": dict(groups.most_common()),
               "complete": not broken and not unclassified and not dup and len(records) > 0,
               "scanned_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    return {"records": records, "receipt": receipt}


def freshness(records) -> dict:
    ids = {r["id"] for r in records}
    out = {}
    smart = jload(SMART, {}) or {}
    out["smart_index"] = {"ok": {p["id"] for p in smart.get("powers", [])} == ids, "fix": "python3 scripts/smart_capabilities.py build"}
    sp = jload(SP, {}) or {}
    members = [m["id"] for s in sp.get("items", []) for m in s.get("pipeline", [])]
    out["superpowers"] = {"ok": set(members) == ids and len(members) == len(set(members)), "fix": "python3 scripts/superpower_fusion.py build"}
    mind = jload(MIND, {}) or {}
    out["mindmap"] = {"ok": set(mind.get("superpowers", {})) == {s["id"] for s in sp.get("items", [])}, "fix": "python3 scripts/capability_mindmap.py build"}
    tools = jload(TOOLS, {}) or {}
    out["tools"] = {"ok": bool(tools.get("tools")), "count": len(tools.get("tools", [])), "fix": "python3 scripts/hub.py build"}
    return out


# ------------------------------------------------------------------ stage 1: request analysis
DELIVERABLES = [
    ("video", r"فيديو|مونتاج|ريلز|موشن|انيميشن|أنيميشن|تحريك|فيلم|video|montage|reel|motion|animation|film|mp4"),
    ("audio", r"صوت|موسيقى|تعليق|بودكاست|audio|music|voice|podcast|wav|mp3"),
    ("image", r"صورة|صور|تصميم|بوستر|شعار|لوجو|image|photo|poster|logo|design|png|jpg"),
    ("3d", r"ثلاثي|3d|بلندر|blender|glb|three"),
    ("code", r"كود|برمجة|تطبيق|موقع|سكربت|bug|code|app|website|script|api|repo|مستودع"),
    ("document", r"تقرير|مستند|وورد|pdf|عرض|شرائح|report|document|docx|slides|deck"),
    ("data", r"بيانات|تحليل|اكسل|جدول|data|csv|excel|chart|dashboard|محاسب"),
    ("research", r"ابحث|بحث|مصادر|research|sources|compare|قارن"),
    ("reverse", r"هندسة عكسية|جفرا|ghidra|\brea\b|reverse|binary|exe|dll|apk"),
]


def analyse(task: str) -> dict:
    low = norm_ar(task.lower())
    deliver = [k for k, rx in DELIVERABLES if re.search(rx, low)]
    numbers = re.findall(r"\b\d+(?:[.,]\d+)?\s*(?:ث|ثانية|ثواني|دقيقة|دقائق|s|sec|min|fps|p|%|k)?\b", task)
    aspects = re.findall(r"\b(?:9:16|16:9|1:1|4:5|21:9|4:3)\b", task)
    paths = [w for w in re.findall(r"[\w./\\:-]+\.(?:mp4|mov|wav|mp3|m4a|png|jpg|jpeg|pdf|docx|xlsx|csv|json|py|js|ts|blend|glb|exe|dll|apk)", task, re.I)]
    existing = [p for p in paths if Path(p).expanduser().exists()]
    try:
        sug = P.suggest(P.load_powers(), [], task, 30)
        intents = {"families": sug["intent"]["families"], "domains": sug["intent"]["domains"]}
    except Exception:  # noqa: BLE001
        intents = {}
    level = "max" if any(h in low for h in MAX_HINTS) else ("fast" if any(h in low for h in FAST_HINTS) else "balanced")
    trivial = len(tokens(task)) <= 3 and not deliver
    questions = []
    if "video" in deliver and not aspects:
        questions.append("المقاس والمنصة (9:16 ريلز؟ 16:9 يوتيوب؟)")
    if deliver and not existing:
        questions.append("هل توجد ملفات مصدر (صوت/فيديو/صور/كود) أرفقها أو مساراتها؟")
    if "video" in deliver and not numbers:
        questions.append("المدة المطلوبة تقريبًا")
    return {"request": task, "deliverables": deliver or ["unspecified"], "constraints": {"numbers": numbers, "aspects": aspects},
            "files_mentioned": paths, "files_found": existing, "intent": intents, "ambition": level, "trivial": trivial,
            "open_questions": questions,
            "claude_must_answer": ["ماذا يريد حرفيًا؟", "ما النتيجة النهائية المتوقعة؟", "ما المشكلة الأساسية؟", "المتطلبات الصريحة والضمنية",
                                   "مستوى الجودة", "القيود الفنية والزمنية والمالية", "معايير نجاح قابلة للقياس", "هل توجد طريقة أذكى من وصف المستخدم؟"]}


# ------------------------------------------------------------------ stage 3: rank everything
def rank_records(records, query_words):
    df = collections.Counter()
    toks = []
    for r in records:
        t = collections.Counter(tokens(r["text"]))
        toks.append(t)
        for w in t:
            df[w] += 1
    n = len(records)
    qset = [w for w in dict.fromkeys(norm_ar(w) for w in query_words)]
    scores = []
    for r, t in zip(records, toks):
        name = set(tokens(r["name_en"] + " " + r["name_ar"]))
        s = 0.0
        for w in qset:
            tf = t.get(w, 0)
            if not tf:
                tf = sum(c for k, c in t.items() if len(w) >= 4 and k.startswith(w))
            if tf:
                idf = math.log(1 + n / (1 + df.get(w, 0)))
                s += (1 + math.log(1 + tf)) * idf * (2.2 if w in name else 1.0)
        scores.append(s)
    return scores


def build_brief(task: str, details=False) -> dict:
    t0 = time.time()
    scan = scan_catalog()
    records, receipt = scan["records"], scan["receipt"]
    fresh = freshness(records)
    an = analyse(task)
    q = expand(task)
    scores = rank_records(records, q)
    by_id = {r["id"]: (r, s) for r, s in zip(records, scores)}
    relevant = [(s, r) for r, s in zip(records, scores) if s > 0]
    relevant.sort(key=lambda x: (-x[0], x[1]["id"]))
    top_s = relevant[0][0] if relevant else 1.0
    # groups
    gsc = collections.Counter()
    for s, r in relevant[:400]:
        gsc[r["group"]] += s
    # superpowers
    sp = jload(SP, {"items": []})
    mind = jload(MIND, {}) or {}
    stage_of = {k: v.get("stage") for k, v in (mind.get("superpowers") or {}).items()}
    hub_of = {k: v.get("hub") for k, v in (mind.get("superpowers") or {}).items()}
    import smart_capabilities as SC
    fam2group = {f.strip(): slug for slug, _a, _e, csv, _k in SC.SPEC for f in csv.split(",")}
    sp_rows = []
    for s in sp.get("items", []):
        ms = [by_id[m["id"]] for m in s["pipeline"] if m["id"] in by_id]
        rel = sorted((sc for _r, sc in ms), reverse=True)
        fit = sum(rel[:5]) + 0.25 * sum(rel[5:])
        if fit <= 0:
            continue
        hits = [r["id"] for r, sc in ms if sc > 0]
        group = collections.Counter(fam2group.get(f) for f in s.get("families", {})).most_common(1)[0][0]
        sp_rows.append({"id": s["id"], "name_ar": s["name_ar"], "name_en": s["name_en"], "group": group, "stage": stage_of.get(s["id"], "create"),
                        "size": s["size"], "best": s["best"], "ready_now": s["ready_now"], "status_mix": s["status_mix"], "requires": s.get("requires", []),
                        "links": [l["id"] for l in s.get("links", [])], "fit_raw": fit, "hits": hits, "twins": s.get("twins", [])})
    sp_rows.sort(key=lambda x: -x["fit_raw"])
    short = sp_rows[:60]
    short_ids = {x["id"] for x in short}
    # requirement presence
    try:
        import requirements as R
        reg = R.registry()
        pres = R.present(reg)
    except Exception:  # noqa: BLE001
        reg, pres = {}, {}
    top_groups = [g for g, _ in gsc.most_common(2)]
    maxfit = max([x["fit_raw"] for x in short] or [1.0])
    for x in short:
        integ = len([l for l in x["links"] if l in short_ids])
        miss = [k for k in x["requires"] if pres.get(k) == "missing"]
        keys = [k for k in x["requires"] if str(k).startswith("key:")]
        feas = (x["ready_now"] / max(1, x["size"])) * 0.6 + (0.4 if not miss else 0.4 * (1 - len(miss) / max(1, len(x["requires"]))))
        sc = {"fit": x["fit_raw"] / maxfit, "integration": min(1.0, integ / 3), "feasibility": feas,
              "evidence": EVIDENCE.get(x["best"], 0.2), "cost": 1.0 - min(1.0, 0.25 * len(miss) + 0.5 * len(keys)),
              "creativity": 1.0 if x["group"] not in top_groups else 0.3}
        x["score"] = round(sum(WEIGHTS[k] * v for k, v in sc.items()), 1)
        x["score_parts"] = {k: round(WEIGHTS[k] * v, 1) for k, v in sc.items()}
        x["missing"] = miss
        x["needs_key"] = keys
        x["role"] = "core" if x["group"] in top_groups else "cross-domain"
    short.sort(key=lambda x: -x["score"])
    # complements: neighbours of the top core picks not yet selected, and a verifier from the quality group
    comp = []
    relevant_sp = {x["id"]: x for x in sp_rows}
    for x in short[:8]:
        for l in x["links"]:
            # a complement must be linked to a top pick AND relevant to the request itself
            if l not in short_ids and l in relevant_sp and l not in [c["id"] for c in comp]:
                s = relevant_sp[l]
                comp.append({"id": l, "name_ar": s["name_ar"], "name_en": s["name_en"], "because": f"linked to {x['id']}", "stage": s["stage"]})
    verifiers = [x for x in short if x["group"] == "quality"][:2] or [x for x in sp_rows if x["group"] == "quality"][:2]
    # tools
    tools_hit = []
    try:
        r = subprocess.run([sys.executable, str(HERE / "hub.py"), "find", task, "--json"], capture_output=True, text=True, timeout=120)
        hf = json.loads(r.stdout)
        tools_hit = [{"id": t["id"], "title_ar": t.get("title_ar"), "title_en": t.get("title_en"), "area": t.get("area"),
                      "state": (t.get("readiness") or {}).get("state"), "missing": (t.get("readiness") or {}).get("missing", []),
                      "command": (t.get("commands") or [{}])[0].get("example") if t.get("commands") else t.get("command")} for t in hf.get("tools", [])[:12]]
        guides = [g.get("path") for g in hf.get("guides", [])[:6]]
    except Exception as exc:  # noqa: BLE001
        guides = [f"hub.py find failed: {exc}"]
    readiness = tool_readiness()
    # plans
    def per_stage(rows, k):
        st = collections.OrderedDict((s, []) for s in STAGE_ORDER)
        for x in rows:
            st.setdefault(x["stage"] or "create", []).append(x)
        return collections.OrderedDict((s, v[:k]) for s, v in st.items() if v)

    def plan(name, rows, k, tools_n, extra_verify, note):
        stages = per_stage(rows, k)
        chosen = [x for v in stages.values() for x in v]
        if extra_verify:
            for v in verifiers[:extra_verify]:
                if v["id"] not in [c["id"] for c in chosen]:
                    chosen.append(v)
                    stages.setdefault("verify", []).append(v)
        stages = collections.OrderedDict((s, stages[s]) for s in STAGE_ORDER if s in stages)
        atoms = sorted({h for x in chosen for h in x["hits"]})
        members = sum(x["size"] for x in chosen)
        req = sorted({k for x in chosen for k in x["requires"]})
        missing = [k for k in req if pres.get(k) == "missing"]
        keys = [k for k in req if str(k).startswith("key:")]
        groups = sorted({x["group"] for x in chosen})
        tl = tools_hit[:tools_n]
        doc_share = sum(1 for x in chosen if x["best"] in ("documented", "idea")) / max(1, len(chosen))
        risks = []
        if missing:
            risks.append(f"{len(missing)} متطلبات ناقصة: " + ", ".join(missing[:6]))
        if keys:
            risks.append("يحتاج مفاتيح/خدمات مدفوعة: " + ", ".join(keys[:4]))
        if doc_share > 0.4:
            risks.append(f"{int(doc_share * 100)}% من القدرات المختارة موصوفة فقط (📄) وتحتاج تنفيذًا")
        return {"name": name, "idea": note, "superpowers": [{"id": x["id"], "name_ar": x["name_ar"], "name_en": x["name_en"], "stage": x["stage"],
                                                                "group": x["group"], "score": x.get("score"), "best": x["best"]} for x in chosen],
                "stages": {s: [x["id"] for x in v] for s, v in stages.items()},
                "counts": {"superpowers": len(chosen), "powers_matched": len(atoms), "powers_in_scope": members, "groups": len(groups),
                           "tools": len(tl), "tools_ready": sum(1 for t in tl if t["state"] == "ready")},
                "groups": groups, "tools": tl, "requires": req, "missing": missing, "keys": keys, "risks": risks or ["لا مخاطر ظاهرة من البيانات"]}

    core = [x for x in short if x["role"] == "core"]
    planA = plan("A", core, 1, 3, 1, "أقل مجموعة تغطي كل مرحلة مطلوبة بأعلى قدرة جاهزة في كل مرحلة + بوابة تحقق واحدة")
    planB = plan("B", short[:30], 3, 6, 2, "أفضل توازن: نواة المجالين الأقوى + قدرات تكامل وتحسين من مجالات أخرى + بوابة تحقق")
    planC = plan("C", short + [x for x in sp_rows[60:] if x["fit_raw"] > 0.35 * maxfit], 6, 12, 2,
                 "كل القدرات ذات الصلة المثبتة عبر كل المجموعات، مراحل بنقاط توقف واختبارات")
    rec = {"fast": "A", "max": "C"}.get(an["ambition"], "B")
    if an["trivial"]:
        rec = "A"
    brief = {"schema": "kosif.skill-intelligence.v1", "protocol": "PROTOCOL.md", "elapsed_s": None,
             "environment": environment(), "freshness": fresh, "coverage": receipt, "analysis": an, "query_terms": q[:40],
             "inventory": {"powers_total": receipt["records_on_disk"], "powers_relevant": len(relevant), "superpowers_total": len(sp.get("items", [])),
                           "superpowers_relevant": len(sp_rows), "shortlist": len(short), "groups_total": receipt["groups"], "families": receipt["families"],
                           "tools_total": readiness["summary"].get("tools"), "tools_ready": readiness["summary"].get("ready"),
                           "groups_ranked": [{"group": g, "score": round(v, 1)} for g, v in gsc.most_common()]},
             "top_powers": [{"id": r["id"], "name_ar": r["name_ar"], "name_en": r["name_en"], "group": r["group"], "status": r["status"], "score": round(s, 2)}
                            for s, r in relevant[:40]],
             "shortlist": short, "complements": comp[:12], "verifiers": [v["id"] for v in verifiers], "tools": tools_hit, "guides": guides,
             "plans": {"A": planA, "B": planB, "C": planC}, "recommended": rec,
             "approval_question": f"أنصحك بالخطة {rec}. تحب أعرض لك تفاصيل القدرات وخطوات التنفيذ، ولا توافق على الخطة ونبدأ مباشرة؟",
             "reply_words": {"موافق": "نفّذ الخطة الموصى بها", "تفاصيل": "جدول أعمق للقدرات والتسلسل والاعتماديات والاختبارات",
                             "A/B/C": "اعتمد خطة أخرى", "طوّر": "جولة نقد وتحسين وبحث عن تكاملات جديدة",
                             "نفّذ بأقصى قوة": "أعلى مستوى عملي دون التضحية بالاختبارات والترخيص", "نفّذ مباشرة": "تخطَّ العرض للمهام البسيطة"}}
    brief["elapsed_s"] = round(time.time() - t0, 2)
    if not details:
        for x in brief["shortlist"]:
            x.pop("hits", None)
            x.pop("twins", None)
    return brief


# ------------------------------------------------------------------ report
def render(b: dict) -> str:
    c, inv, an = b["coverage"], b["inventory"], b["analysis"]
    B = P.BADGE
    L = ["# تقرير بروتوكول ذكاء المهارات — KOSIF USIP", "", f"**الطلب:** {an['request']}", "",
         "## أولًا — فهم الطلب (مسودة آلية يكملها Claude بتفكيره)", "",
         f"- المخرجات المرجحة: {', '.join(an['deliverables'])} · الطموح: {an['ambition']}" + (" · طلب بسيط → مسار مختصر" if an["trivial"] else ""),
         f"- قيود مذكورة: أرقام {an['constraints']['numbers'] or '—'} · مقاسات {an['constraints']['aspects'] or '—'} · ملفات موجودة {an['files_found'] or '—'}",
         "- أسئلة مفتوحة: " + (" · ".join(an["open_questions"]) or "—"), "",
         "## ثانيًا — نتيجة جرد المهارات", "",
         f"| البند | العدد |", "|---|---|",
         f"| إجمالي القدرات في الفهرس | {c['records_on_disk']:,} |",
         f"| السجلات التي فُحصت آليًا (100%) | {c['records_scanned']:,} {'✅' if c['complete'] else '❌ غير مكتمل'} |",
         f"| المجموعات / العائلات المغطاة | {c['groups']} / {c['families']} |",
         f"| القدرات ذات الصلة بالطلب | {inv['powers_relevant']:,} |",
         f"| القدرات الخارقة ذات الصلة / في قائمة الترشيح | {inv['superpowers_relevant']} / {inv['shortlist']} |",
         f"| سجلات تالفة أو غير مصنفة | {c['broken_count']} / {c['unclassified_count']} |",
         f"| الأدوات القابلة للتشغيل الآن | {inv['tools_ready']} من {inv['tools_total']} |",
         f"| بصمة الكتالوج | `{c['catalog_sha256'][:16]}…` |", "",
         "حداثة الفهارس: " + " · ".join(f"{k} {'✅' if v.get('ok') else '❌ → ' + v.get('fix', '')}" for k, v in b["freshness"].items()), "",
         "المجموعات الأقرب: " + " · ".join(f"{g['group']} ({g['score']})" for g in inv["groups_ranked"][:6]), "",
         "## ثالثًا — مقارنة الخطط", "",
         "| البند | الخطة A — ذكية سريعة | الخطة B — احترافية متوازنة | الخطة C — قصوى ابتكارية |", "|---|---|---|---|"]
    pl = b["plans"]
    row = lambda label, f: L.append(f"| {label} | " + " | ".join(f(pl[k]) for k in "ABC") + " |")
    row("الفكرة الأساسية", lambda p: p["idea"])
    row("القدرات الخارقة", lambda p: str(p["counts"]["superpowers"]))
    row("القدرات المطابقة / في النطاق", lambda p: f"{p['counts']['powers_matched']} / {p['counts']['powers_in_scope']}")
    row("الأدوات التنفيذية (جاهزة)", lambda p: f"{p['counts']['tools']} ({p['counts']['tools_ready']})")
    row("المجموعات", lambda p: ", ".join(p["groups"]))
    row("متطلبات ناقصة", lambda p: str(len(p["missing"])))
    row("المخاطر", lambda p: " · ".join(p["risks"])[:160])
    L += ["", "### مراحل كل خطة", ""]
    for k in "ABC":
        p = pl[k]
        L.append(f"**الخطة {k}:** " + " ← ".join(f"{s}: " + ", ".join(p["stages"][s]) for s in p["stages"]))
    L += ["", "## رابعًا — قائمة الترشيح (أعلى 15 بالنقاط من 100)", "", "| SP | القدرة الخارقة | المجموعة | المرحلة | الدرجة | أفضل شارة | الدور |", "|---|---|---|---|---|---|---|"]
    for x in b["shortlist"][:15]:
        L.append(f"| {x['id']} | {x['name_ar']} · {x['name_en']} | {x['group']} | {x['stage']} | {x['score']} | {B.get(x['best'], '')} | {x['role']} |")
    if b["tools"]:
        L += ["", "**أدوات قابلة للتشغيل:** " + " · ".join(f"`{t['id']}` ({t['state']})" for t in b["tools"][:8])]
    if b["complements"]:
        L += ["", "**مكمّلات مقترحة من الروابط:** " + " · ".join(f"{c['id']} {c['name_ar']}" for c in b["complements"][:6])]
    L += ["", f"## خامسًا — التوصية: الخطة {b['recommended']}", "",
          "(Claude: اشرح لماذا هي الأفضل لهذا الطلب، أبرز القدرات، الفرق عن الحل التقليدي، ومعايير النجاح القابلة للتحقق.)", "",
          f"**{b['approval_question']}**", "", "ردود بكلمة واحدة: " + " · ".join(f"`{k}`" for k in b["reply_words"]), ""]
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("brief"); b.add_argument("task"); b.add_argument("--json", action="store_true"); b.add_argument("--out", type=Path)
    b.add_argument("--details", action="store_true")
    sub.add_parser("verify")
    a = ap.parse_args(argv)
    if a.cmd == "verify":
        scan = scan_catalog()
        fr = freshness(scan["records"])
        ok = scan["receipt"]["complete"] and all(v.get("ok") for v in fr.values())
        print(json.dumps({"pass": ok, "coverage": {k: v for k, v in scan["receipt"].items() if k != "group_sizes"}, "freshness": fr}, ensure_ascii=False, indent=1))
        return 0 if ok else 1
    br = build_brief(a.task, a.details)
    if a.out:
        a.out.write_text(json.dumps(br, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(br, ensure_ascii=False, indent=1) if a.json else render(br))
    return 0 if br["coverage"]["complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
