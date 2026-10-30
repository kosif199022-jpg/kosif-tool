#!/usr/bin/env python3
"""KOSIF Universal Skill Intelligence Protocol — محرك بروتوكول ذكاء المهارات الشامل (implements USIP v6.0).

The machine half of PROTOCOL.md. For any request it:
  0. checks the environment and that every derived index is fresh,
  1. drafts a request card: protocol level (L0–L3; a question, definition or how-to is L0 even when it names a
     video or code term), intent (produce, or publish something that exists), deliverable, style, topics,
     constraints, own-asset rules (ownership forms only), must-haves (each with deliverable-specific search terms;
     a GitHub push only on a push intent) and the questions that change the result, each with a suggested default,
  2. scans 100% of the catalog records (every data/powers/*.json row) and returns a SHA-256 coverage receipt
     that fails closed when any record is unreadable, unclassified or duplicated,
  3. ranks groups, fused superpowers, powers and runnable tools by query CONCEPTS (a word, its aliases and its
     clitic stem count once; homonyms are resolved by the SENSE table; a superpower's size does not buy rank);
     a must-have layer forces in what the request cannot do without (through a family that can meet the need for
     this deliverable, else an honest gap), a constraint layer excludes what would replace the user's own assets,
     a fit floor (MIN_FIT x best fit) keeps unrelated picks out of plans, and a superpower built around one named
     platform (Godot, Shopify, App Store, EVM, GitHub Actions, JEB, MongoDB…) needs that platform in the request,
  4. scores candidates (fit 35 · integration 20 · feasibility 15 · evidence 10 · cost 10 · creativity 10) with
     LOCAL badges (proof in this checkout, requirements present here); below the fit floor every non-fit part
     scales with fit, and a cross-domain integration never comes from a group that is off-domain for the deliverable,
  5. picks verifiers per deliverable and per request (best atom + 0.25 x next three, weighted by how much the
     checker also matches the request, a family whitelist, no sound checks for a silent deliverable and a dedicated
     loudness check for one that carries sound) and drafts plans A/B/C as different APPROACHES for the deliverable
     type (A = simplest path that meets every must-have, B = balanced professional with cross-domain integration,
     C = different engine, source or verification method, not B plus extras: C reuses at most half of B's own picks
     and has picks of its own, else it is labelled a depth level of B, else marked unavailable), each covering every
     must-have and ending in a verifier, with counts, risks, a recommendation and its reason, and the approval question.

  python3 skill_intelligence.py brief "<request>" [--terms "english keywords"] [--json] [--out FILE] [--details]
  python3 skill_intelligence.py count --sp SP-0001,SP-0002 [--atoms ID,...] [--tools id,...]   # counts for an edited plan
  python3 skill_intelligence.py deep SP-0001 ARAB-12 montage-pro ...                            # cards in one call
  python3 skill_intelligence.py verify                                                          # coverage + freshness (exit 1 on a gap)

Read-only: it never executes a catalog capability, installs anything or contacts the network. The plans are a
draft for Claude to think over and replace with its own approaches; the user's one-word answer decides what runs.
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
QPACKS = SKILL / "data" / "question_packs.json"   # story/scene intake (A17): questions with defaults, inside the report
WEIGHTS = {"fit": 35, "integration": 20, "feasibility": 15, "evidence": 10, "cost": 10, "creativity": 10}
LOCAL_RANK = ["✅", "🟢", "📦", "🔑", "📄", "💡"]
LOCAL_EVIDENCE = {"✅": 1.0, "🟢": 0.8, "📦": 0.55, "🔑": 0.4, "📄": 0.25, "💡": 0.1}
STAGE_ORDER = ["understand", "plan", "create", "refine", "assemble", "verify", "deliver"]
PROTOCOL_VERSION = "USIP v6.0"
META_TOOL_RX = re.compile(r"^(capability-|atlas-|ai-tool-discovery|boot|hub$|powers|skill-intelligence|superpower-fusion|kosif-groups|capability|requirements|probe-env|catalog-|check-skill|relabel|build-chapters|package-skill|rea-creative)")
MIN_FIT = 0.25          # a non-must-have pick needs at least this share of the best fit to enter a plan or be "core"
PLAN_DEFINITIONS = {    # canonical one-line meanings (CONTRACT glossary); Phase 6 of PROTOCOL.md is the source
    "A": "simplest path that meets every must-have", "B": "balanced professional with cross-domain integration",
    "C": "different engine, source or verification method (not B plus extras)", "D": "user-approved merge of named nodes from A/B/C"}


# ------------------------------------------------------------------ text
def norm_ar(s: str) -> str:
    s = re.sub(r"[ً-ْـ]", "", s or "")
    return s.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا").replace("ة", "ه").replace("ى", "ي")


_STOP_RAW = ("the and for with from that this your make build want need what how please a an is are of to my can i you me it in on "
             "عايز اعمل عمل من في على عن الى إلى و ال دي ده دول هذا هذه لي هل ممكن اريد أريد ابغى ابي عاوز يا مع كل بعد قبل "
             "فيه يكون ابني صغير بسيط بسيطة عندي عشان علشان بتاع بتاعي اللي الذي التي انا أنا لو او أو ثم كده كدا ازاي إزاي "
             "create ملف طلع وطلع الـ طور افضل احسن بين بينها best طويل طويله مفصل")
STOP = {norm_ar(w) for w in _STOP_RAW.split()}
ALIASES = {  # protocol-specific Arabic/Egyptian → English bridges (checked against catalog wording)
    "محاسبه": "accounting bookkeeping ledger", "محاسبة": "accounting bookkeeping ledger", "مخزون": "inventory stock sku",
    "مبيعات": "sales", "تقرير": "report", "شهري": "monthly", "فاتوره": "invoice", "فواتير": "invoice",
    "ترجم": "translate translation", "ترجمه": "translation subtitles captions", "فويس": "voice narration audio", "صوتي": "voice narration audio",
    "بصوتي": "voice narration audio", "تطبيق": "app application", "اختبارات": "tests testing", "اختبار": "test testing",
    "شخصيه": "character", "ابحث": "search research", "دور": "search", "كرتونيه": "cartoon character", "كرتوني": "cartoon character", "ريلز": "reels vertical short",
    "موشن": "motion graphics animation", "جرافيك": "graphics", "متحركه": "animated kinetic", "كلمات": "words captions kinetic typography",
    "عربيه": "arabic", "عربي": "arabic", "ميزه": "feature", "ميزة": "feature", "مشابهه": "similar original", "مشابهة": "similar original",
    "حلل": "analyze analysis", "هندسه": "engineering", "عكسيه": "reverse", "مثبت": "installed", "مسار": "path",
    "مونتاج": "montage edit cut", "فيديو": "video", "صوره": "image photo", "صور": "images photos", "رسم": "draw drawing",
    "ارسم": "draw", "خط": "font typography", "خطوط": "fonts typography", "فونت": "font typeface", "كوفي": "kufi arabic font",
    "ديواني": "diwani calligraphy", "بوستر": "poster", "لوجو": "logo brand", "شعار": "logo brand", "بيانات": "data", "مستند": "document", "بحث": "search research",
    "بروتوكول": "protocol", "تفريغ": "transcription transcribe speech-to-text whisper asr", "تفريغه": "transcription transcribe speech-to-text whisper asr",
    "مقال": "article essay", "مقاله": "article essay", "قارن": "compare comparison benchmark", "مقارنه": "compare comparison benchmark",
    "مكتبات": "libraries packages", "داشبورد": "dashboard", "اختبر": "test testing", "مهارات": "skills", "سكيل": "skill",
    "اكسل": "excel spreadsheet xlsx", "جدول": "table spreadsheet", "ويب": "web frontend backend", "اداره": "management crud admin",
    "ثلاثي": "3d", "ثلاثيه": "3d", "ابعاد": "3d", "تمشي": "walk walking", "يمشي": "walk walking", "مشي": "walk walking",
    "مشهد": "scene", "سينمائي": "cinematic", "حرك": "animate animation",
    "مصاريف": "expense expenses budget spending", "مصروفات": "expense expenses budget spending", "نفقات": "expense expenses budget spending",
    "ميزانيه": "budget expense", "لعبه": "game", "العاب": "game games", "قواعد": "rules",
    # everyday business, data-cleaning, bug-fix and contract words (generalization set, evals/routing_generalization.json)
    "تسويق": "marketing go-to-market", "تسويقيه": "marketing go-to-market", "جدوي": "feasibility business case unit economics",
    "تسعير": "pricing price", "اسعر": "pricing price", "اسعار": "pricing price", "سعر": "pricing price",
    "منافسين": "competitors competitive analysis", "المنافسين": "competitors competitive analysis", "تنافسيه": "competitive advantage positioning",
    "ارباح": "profit margin revenue", "الارباح": "profit margin revenue", "ايرادات": "revenue", "عملاء": "customers", "مشروع": "project business",
    "نظف": "clean cleaning", "تنظيف": "clean cleaning", "تكرار": "duplicates deduplicate dedupe", "التكرار": "duplicates deduplicate dedupe",
    "مكرر": "duplicates deduplicate", "لخص": "summarize summary", "ملخص": "summary summarize",
    "عقد": "contract legal clauses", "العقد": "contract legal clauses", "بنود": "clauses contract terms", "البنود": "clauses contract terms",
    "بج": "bug debug fix", "البج": "bug debug fix", "باج": "bug debug fix", "صلح": "fix debug", "موبايل": "mobile responsive",
    "ثغرات": "vulnerabilities security", "امنيه": "security",
}
# homonyms whose dominant catalog sense differs from the user's. Each entry is (rules, default): a rule is
# (context regex on the request, terms, keep_word) and the first rule whose context matches wins; otherwise the default
# (terms, keep_word) applies. keep_word=False drops the bare word (its catalog sense is the wrong one). Checked against
# catalog wording; tests cover the opposite sense of every entry.
_GIT_CTX = r"github|جيت ?هب|\bgit\b|مستودع|ريبو|\brepo\b|pull request|طلب دمج|\bbranch\b|فرع|\bcommits?\b"
_CI_CTX = r"github actions|\bci\b|yaml|\.github|\bactions?\b|n8n|zapier|airflow|\bdags?\b"
SENSE = {
    "workflows": ([(_CI_CTX, "", True)], ("orchestration multi-agent", False)),
    "workflow": ([(_CI_CTX, "", True)], ("orchestration multi-agent", False)),
    "ارفع": ([(_GIT_CTX, "github commit branch", False), (r"جوده|دقه|وضوح|quality|resolution|\bres\b", "upscale enhance quality", False)],
             ("upload publish", False)),
    "push": ([(_GIT_CTX, "git github commit", False)], ("", True)),           # otherwise the camera sense («camera push»)
    "محرك": ([(r"usip|fusionforge|بروتوكول|protocol|مهار(?:ه|ات)|سكيل|skills?\b|\bagents?\b|وكيل|وكلاء|workflow|توليف|orchestr", "orchestration", False)],
             ("engine", True)),                                              # a game, search, rules or render engine stays an engine
    "تسجيل": ([(r"دخول|login|sign ?in|حساب|مستخدم", "login authentication", False),
               (r"شاشه|screen|صوت|audio|voice|فيديو|video|مايك|mic", "recording", True),
               (r"مصاريف|مصروفات|نفقات|حضور|يومي|بيانات|expense|budget", "log tracking record", False)],
              ("log record", True)),
}


def tokens(s: str) -> list:
    s = norm_ar(str(s or "").lower())
    s = re.sub(r"[،؛؟٪-٭۔«»“”\"'(),.:;!?،]", " ", s)
    return [w for w in re.findall(r"[a-z0-9][a-z0-9+#-]*[a-z0-9+#]|[a-z0-9]|[ء-يٱ-ۓ]{2,}", s) if w not in STOP]


def _stems(w: str) -> list:
    """Clitic stems of an Arabic word: one leading clitic (و/ب/ل/ف/ال…) and/or one trailing pronoun (ه/ها/هم)."""
    out = []
    for pre in ("وال", "بال", "فال", "لل", "ال", "و", "ب", "ل", "ف"):
        if w.startswith(pre) and len(w) - len(pre) >= 3:
            out.append(w[len(pre):])
            break
    for x in [w] + out:
        for suf in ("ها", "هم", "ه"):
            if x.endswith(suf) and len(x) - len(suf) >= 3:
                out.append(x[:-len(suf)])
                break
    return out


def _concept(w: str, df, ctx: str) -> list:
    """One request word as a concept: the word, its clitic stem (when only the stem is in the catalog), its aliases,
    or the SENSE replacement when the catalog's dominant sense is not the user's."""
    base = w
    if re.match(r"[؀-ۿ]", w) and w not in ALIASES and w not in SENSE:
        stems = _stems(w)
        known = next((st for st in stems if st in ALIASES or st in SENSE), None)
        if known:
            base = known
        elif df.get(w, 0) < 3:   # a clitic form the catalog barely uses: score its stem
            base = next((st for st in stems if df.get(st, 0) > max(2, df.get(w, 0))), w)
    if base in SENSE:
        rules, default = SENSE[base]
        terms, keep = next(((t, k) for rx, t, k in rules if re.search(rx, ctx)), default)
        group = ([w, base] if keep else []) + tokens(terms)
    else:
        group = [w, base] + tokens(ALIASES.get(base, ""))
    return [x for x in dict.fromkeys(group) if x and x not in STOP]


def concepts(query: str, df: collections.Counter, extra: str = "") -> list:
    """Query concepts (lists of interchangeable terms). A word and its alias are one concept, so an Arabic word and its
    English translation do not score twice; concepts that share a term are merged."""
    ctx = norm_ar(f"{query} {extra}".lower())
    groups = []
    for w in tokens(query) + tokens(extra):
        g = _concept(w, df, ctx)
        if not g:
            continue
        for h in groups:
            if set(h) & set(g):
                h.extend(x for x in g if x not in h)
                break
        else:
            groups.append(g)
    return groups


def expand(query: str, df: collections.Counter, extra: str = "") -> list:
    """Query words + aliases + clitic stems + SENSE rewrites, flattened (the terms of concepts())."""
    return list(dict.fromkeys(x for g in concepts(query, df, extra) for x in g))


def jload(p: Path, default=None):
    try:
        return json.loads(p.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        return default


# ------------------------------------------------------------------ stage 0
def environment() -> dict:
    env = {"python": sys.version.split()[0], "tools": {b: bool(shutil.which(b)) for b in ("ffmpeg", "ffprobe", "node", "git", "rea", "blender", "yt-dlp")}}
    if not env["tools"]["yt-dlp"]:  # pip may install the module without putting the CLI on PATH
        import importlib.util  # noqa: PLC0415
        env["tools"]["yt-dlp"] = importlib.util.find_spec("yt_dlp") is not None
    try:
        r = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True, timeout=10)
        env["git_branch"] = r.stdout.strip() or None
        r = subprocess.run(["git", "-C", str(REPO), "status", "--porcelain"], capture_output=True, text=True, timeout=20)
        env["git_dirty_files"] = len([l for l in r.stdout.splitlines() if l.strip()])
    except (OSError, subprocess.TimeoutExpired):
        env["git_branch"] = None
    return env


def tool_registry() -> dict:
    t = jload(TOOLS, {}) or {}
    return {x["id"]: x for x in t.get("tools", [])}


def tool_readiness() -> dict:
    try:
        r = subprocess.run([sys.executable, str(HERE / "hub.py"), "doctor", "--json"], capture_output=True, text=True, timeout=120)
        d = json.loads(r.stdout)
        return {"summary": d.get("summary", {}), "state": {t["id"]: t.get("state") for t in d.get("tools", [])}}
    except Exception as exc:  # noqa: BLE001
        return {"summary": {"error": str(exc)[:200]}, "state": {}}


def requirement_presence():
    try:
        import requirements as R
        reg = R.registry()
        return reg, R.present(reg)
    except Exception:  # noqa: BLE001
        return {}, {}


# ------------------------------------------------------------------ stage 2: coverage
def sha_catalog():
    h = hashlib.sha256()
    files = sorted(POWERS.glob("*.json"))
    for f in files:
        h.update(f.name.encode())
        h.update(f.read_bytes())
    return h.hexdigest(), len(files)


def fam_to_group() -> dict:
    import smart_capabilities as SC
    return {f.strip(): slug for slug, _a, _e, csv, _k in SC.SPEC for f in csv.split(",")}


# planning labels: where a family really belongs when choosing an approach (the smart index keeps its own grouping)
PLAN_GROUP = {"engines-render-pipeline": "motion", "light-glow-bloom": "motion", "particles-fluids-physics": "motion",
              "color-palette-grading": "motion", "photo-video-footage": "motion", "ui-product-device": "motion"}
TOOL_AREA_GROUP = {"motion": "motion", "edit": "motion", "audio": "audio", "draw": "drawing", "3d": "3d", "image": "images",
                   "sources": "motion", "investigate": "reverse", "think": "thinking", "discover": "agents", "maintain": "quality",
                   "local-computer": "agents"}


def scan_catalog() -> dict:
    """Read every record of every data/powers/*.json; classify each into its group; fail closed on any gap."""
    fam2group = fam_to_group()
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
                            "status": r.get("status"), "proof_scope": r.get("proof_scope") or "none",
                            "name_en": r.get("name_en", ""), "name_ar": r.get("name_ar", ""), "requires": r.get("requires") or [],
                            "tags": " ".join(map(str, r.get("tags") or [])), "section": r.get("section", ""),
                            "text": " ".join([str(r.get("name_en", "")), str(r.get("name_ar", "")), " ".join(map(str, r.get("tags") or [])),
                                              str(r.get("section", "")), str(r.get("when", "")), str(r.get("what", ""))[:400]]),
                            "file": f.name})
    ids = [r["id"] for r in records]
    dup = [k for k, v in collections.Counter(ids).items() if v > 1]
    digest, nfiles = sha_catalog()
    groups = collections.Counter(r["group"] for r in records if r["group"])
    receipt = {"catalog_sha256": digest, "files": nfiles, "records_on_disk": len(records), "records_scanned": len(records),
               "records_classified": sum(1 for r in records if r["group"]), "unclassified": unclassified[:20], "unclassified_count": len(unclassified),
               "broken": broken[:20], "broken_count": len(broken), "duplicate_ids": dup[:20], "families": len({r["family"] for r in records}),
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


# ------------------------------------------------------------------ stage 1: request card
DELIVERABLES = [  # priority order: the first that matches is the primary deliverable
    ("reverse", r"هندسه عكسيه|جفرا|ghidra|\brea\b|reverse|binary|\.exe|\.dll|\.apk|\b(?:exe|dll|apk|ipa|dylib)\b|ملف تنفيذي|الملف التنفيذي|"
                r"(?<![ء-ي])[وف]?فك (?:ال)?(?:تطبيق|ملف|برنامج)|app\.asar|\basar\b|electron|الكترون"),
    ("code", r"كود|برمجه|تطبيق|(?<![ء-ي])[وف]?(?:ال|ل|ب)?موقع(?:ي|نا|ك)?(?![ء-ي])|سكربت|\bbug\b|\bcode\b|\bapp\b|\bwebsites?\b|\bscripts?\b|"
             r"\bapi\b|\brepo(?:s|sitory|sitories)?\b|مستودع|برنامج|بايثون|\bpython\b|\bnode(?:\.?js)?\b|\breact\b|fastapi|django|"
             r"\bbugs?\b|\bdebug|memory leak|\blogin\b|تسجيل (?:ال)?دخول|ايرور|(?<![ء-ي])[وف]?(?:ال)?(?:بج|باج|بق)(?![ء-ي])|"
             r"\bfrontend\b|\bbackend\b|ثغر(?:ه|ات)|(?<![ء-ي])[وف]?(?:ال)?بوت(?![ء-ي])|\b(?:chat)?bots?\b"),
    ("video", r"فيديو|مونتاج|ريلز|موشن|انيميشن|تحريك|(?<![ء-ي])[وف]?(?:حرك|متحرك|متحركه)(?![ء-ي])|فيلم|video|montage|\breels?\b|(?<![a-z])motion|animation|film|\bmp4\b|\bintro\b|انترو|paper edit|rough cut"),
    ("audio", r"بودكاست|موسيقي|اغني(?:ه|تي|ات)|نشيد|اناشيد|تلاوه|podcast|music|song|nasheed|\bsuno\b|سونو|\blyrics?\b|كلمات (?:ال)?اغني(?:ه|تي)"),
    ("3d", r"ثلاثي|\b3d\b|بلندر|blender|\bglb\b|three\.?js"),
    ("image", r"صوره|صور|تصميم|بوستر|شعار|لوجو|بطاقه|كارت|دعوه|غلاف|هويه بصريه|(?<![ء-ي])[وف]?(?:ا)?رسم|ماسكوت|image|photo|poster|logo|design|illustrat|mascot|\bcard\b|invitation|\bcover\b(?!\s+letters?)|\bpng\b|\bjpg\b"),
    # business decisions and plans (marketing, pricing, feasibility, competitors, business plans): a reasoning deliverable
    ("strategy", r"خط(?:ه|ط) (?:تسويق|مبيعات|عمل|نمو|محتوي|توسع)|استراتيجي|دراسه جدوي|جدوي|تسعير|(?<![ء-ي])اسعر(?![ء-ي])|"
                 r"المنافسين|منافسين|ميزه تنافسيه|تنافسي|نموذج (?:عمل|ربح)|\bpric(?:e|es|ing)\b|\bchurn\b|business plan|"
                 r"(?<![ء-ي])[وف]?(?:افتح|ابدا|اطلق)(?:\s+\S+){0,1}\s+(?:محل|كافيه|مطعم|مشروع|شركه|متجر|براند|بيزنس)|"
                 r"\bstart(?:ing)? an? (?:\w+\s+)?(?:business|company|startup|shop|store|cafe)\b|\bstrategy\b|go-to-market|\bgtm\b|feasibility|competitors?\b|\bshould (?:i|we)\b|unit economics|\bmarketing plan\b"),
    ("data", r"بيانات|اكسل|جدول|\bdata\b|\bcsv\b|\bxlsx?\b|excel|chart|dashboard|داشبورد|مبيعات|ارباح|ايرادات|\bsales\b|\brevenue\b|forecast|توقعات|تنبؤ"),
    ("document", r"تقرير|مستند|وورد|\bpdf\b|عرض تقديمي|شرائح|report|document|docx|slides|deck|مقال|article|\bdescriptions?\b|"
                 r"\bemails?\b|ايميل|\bnewsletter\b|\bblog posts?\b|(?<![ء-ي])[وف]?(?:ال)?عقد(?:ه|ها)?(?![ء-ي])|\bcontracts?\b|البنود|بنود|اتفاقي(?:ه|ات)|وصف (?:ال)?منتج|cover letters?|\bpoems?\b|قصيده|خطاب"),
    ("research", r"ابحث|مصادر|research|sources|قارن|compare"),
]
# a weaker code signal: engineering words that make code the deliverable only when nothing stronger is named. The
# ambiguous ones (protocol, engine, workflow, commit: a hotel protocol, a search-engine marketing plan, a morning
# workflow) count only next to a software context word.
META_CODE_RX = (r"github|جيت ?هب|\bgit\b|pull request|\bci\b|سكيل|skill\.md|\b(?:claude|agent|kosif)\s+skills?\b|\bmcp\b|\bcli\b|\bsdk\b")
META_WEAK_RX = (r"بروتوكول|(?<![ء-ي])[وف]?(?:بال|لل|ال|ب|ل)?محرك(?:ات)?(?![ء-ي])|\bprotocol\b|\bengine\b|\bcommits?\b|workflows?\b")
SOFTWARE_CTX_RX = (r"كود|برمج|سكربت|\bscripts?\b|\bcode\b|github|جيت ?هب|\bgit\b|\brepo\b|مستودع|skill|سكيل|مهار(?:ه|ات)|\bmcp\b|\bcli\b|"
                   r"\bsdk\b|\bapi\b|اختبار|اختبر(?!ني|نا)|\btests?\b|pytest|unittest|usip|fusionforge|kosif|claude|\bagents?\b|وكيل|وكلاء|"
                   r"python|بايثون|javascript|typescript|\bnode\b|remotion|\bjson\b|yaml|\bci\b|\bllm\b|توليف")
SHORT_INTENTS = (r"^(ترجم|translate|اشرح|explain|عرف|define|ما معني|ايه معني|وش معني|ايش معني|شو معني|اش معني|ش معني|يعني ايه|يعني ايش|يعني شو|"
                 r"شو يعني|وش يعني|ايش يعني|ما المقصود|ما الفرق|ايه الفرق|وش الفرق|شو الفرق|ما هو|ما هي|ايه هو|ايه هي|ايش هو|ايش هي|وش هو|وش هي|"
                 r"شو هو|شو هي|مين|من هو|من هي|متي|امتي|فين|وين|اين|كم|ليش|ليه|لماذا|ايه (?:احسن|افضل)|"
                 r"what does|what is|what's|whats|what are|who|when|where|why|how many|how much|difference between|the difference|meaning of|"
                 r"صحح|صلح|proofread|rename|اعد صياغه|لخص|summari[sz]e)")
# a definition or how-to question: L0 even when it names a video, code, 3D or reverse-engineering term ("what does API mean?")
DEFINE_RX = (r"^(?:ما معني|ايه معني|وش معني|ايش معني|شو معني|اش معني|يعني ايه|يعني ايش|يعني شو|شو يعني|وش يعني|ايش يعني|ما المقصود|ما الفرق|"
             r"ايه الفرق|وش الفرق|شو الفرق|ما هو|ما هي|ايه هو|ايه هي|ايش هو|وش هو|شو هو|عرف|define|what does|what is|what's|whats|what are|"
             r"meaning of|difference between|the difference|(?:اشرح(?: لي)?|explain)\s+(?:ازاي|كيف|ايه|يعني|what|how|why|the difference|الفرق))")
# an existing artefact of the user's ("this code", «الكود ده»): a question about it is work on it, not a definition
EXISTING_OBJ_RX = (r"\b(?:this|these|my|our|attached)\b|(?<![ء-ي])(?:ده|دي|دا|دول|هذا|هذه|هاد|هاي|عندي|بتاعي|بتاعتي|حقي|تبعي|المرفق)(?![ء-ي])")
# a verb or format that turns an explain/summarise request into production (PROTOCOL.md: such a request is not L0).
# A format counts only as an output: «في مقال» / "in an article" (indefinite), never «في التقرير» / "in the report".
_FMT = r"(?:مقال|مقاله|تقرير|عرض|فيديو|ملف|كتاب|منشور|بوست|pdf|شرائح|انفوجرافيك|ريلز)"
PRODUCE_RX = (r"(?<![ء-ي])[وف]?(?:اعمل|اكتب|صمم|انشر|جهز|حضر|طلع|ارفع|ابني|انتج|صدر|ارسم|اصنع|سوي)(?:ه|ها|هم|لي|لنا)?(?![ء-ي])|"
              r"(?<![ء-ي])[وف]?حول(?:ه|ها|هم|لي)?(?:\s+\S+){0,3}?\s+(?:الي|ل)\s|"     # «حوّله إلى/لـ» converts; «حول» alone is 'about'
              r"\b(?:create|make|write|publish|post|produce|generate|export|build|design|render|convert)\b|"
              rf"(?:علي شكل|في شكل|بشكل|بصيغه|(?<![ء-ي])ك)\s*(?:ال)?{_FMT}(?![ء-ي])|(?<![ء-ي])في\s+{_FMT}(?![ء-ي])(?!\s+ال)|"
              r"\b(?:as|in|into) an? (?:[a-z0-9-]+\s+){0,2}(?:article|report|deck|video|post|pdf|document|slides?|animation|reel|infographic)\b")
HOWTO_RX = r"(?:ازاي|كيف|ازاى|how to|how do i|how can i|how should i|(?:احسن|افضل) (?:وقت|طريقه)(?: ا?ن)?|best (?:time|way) to)\s*$"
RESEARCH_LEAD_RX = r"(?:find|search for|look for|look up|compare|research|ابحث|دور(?:لي| لي)?|قارن)\b"
FAST_RX = r"(بسرعه|نسخه (بسيطه|سريعه)|مختصر|quick version|\bquick\b|\bfast\b|سطر واحد|one line)"
# "max 30 seconds" / "maximum length" is a limit, not an ambition
MAX_RX = (r"(باقصي|اقصي قوه|كل القدرات|\bmax(?:imum)?\b(?!\s*(?:of\s*)?\d|\s+(?:length|duration|size|time|seconds?|minutes?|secs?|mins?|"
          r"chars?|characters|words|width|height|pages?|frames?|files?|budget))|ultimate|best possible)")
# publishing or uploading something that already exists is delivery, not new production
PUBLISH_RX = r"(?<![ء-ي])[وف]?(?:انشر|ارفع|نزل|شير)\S*|\b(?:post|publish|upload|share|push)(?:ed|es|ing)?\b"
PUBLISH_DEST_RX = (r"يوتيوب|youtube|انستا|instagram|\binsta\b|tiktok|تيك ?توك|فيسبوك|facebook|تويتر|twitter|لينكد|linkedin|مدون|\bblog\b|"
                   r"ووردبريس|wordpress|درايف|\bdrive\b|github|جيت ?هب|سناب|snapchat|threads|reddit|medium|substack|\bstore\b|متجر")
PUBLISH_OBJ_RX = (r"\b(?:this|my|our|the|these)\b|(?<![ء-ي])(?:ده|دي|دا|هذا|هذه|بتاعي|بتاعتي)(?![ء-ي])|"
                  r"(?<![ء-ي])[وف]?ال(?:فيديو|مقال|مقاله|ريلز|صوره|صور|بوست|منشور|تعديلات|كود|ملف|تطبيق|موقع)")
NEW_WORK_RX = (r"(?<![ء-ي])[وف]?(?:اعمل|اكتب|صمم|جهز|حضر|ابني|انتج|ارسم|اصنع|سوي|عدل|حرر|طور|حسن|اضف|صلح|اختبر|قص|مونتج|ترجم)"
               r"(?:ه|ها|هم|لي|لنا)?(?![ء-ي])|\b(?:create|make|write|produce|generate|build|design|render|edit|cut|develop|improve|fix|add|"
               r"test|translate|refactor)\b")
# a second piece of work joined to a short intent («ترجم العقد وراجع البنود», "translate and flag the risky clauses"):
# the request is a task with judgement in it, not a one-line dictated edit
COMPOUND_RX = (r"(?<![ء-ي])و(?:راجع|حلل|قيم|اعمل|اكتب|صمم|قارن|اقترح|استخرج|حدد|طلع|افحص|ابحث|نفذ|ابني|صلح|عدل)(?:ه|ها|هم|لي|لنا)?(?![ء-ي])|"
               r"\band (?:then )?(?:review|analy[sz]e|flag|check|assess|compare|suggest|extract|build|write|fix|rewrite)\b")
# a written piece names the deliverable even when its subject is data or sales («ايميل مبيعات», "a sales email")
WRITTEN_PIECE_RX = r"\bemails?\b|ايميل|\bletters?\b|خطاب|\bnewsletter\b|\barticles?\b|مقال|\bblog posts?\b|\bpoems?\b|قصيده"
# a business decision ("should we… or…", «هل… ولا…») about selling, pricing or customers is a strategy job even when
# one option is an app; "should I use React or Vue" has no business word and stays code
DECISION_LEAD_RX = r"\bshould (?:i|we)\b|\bwhether\b|^هل |(?<![ء-ي])ولا(?![ء-ي])|(?<![ء-ي])اختار بين"
BUSINESS_RX = (r"\bsell(?:s|ing)?\b|\bpric(?:e|es|ing)\b|\bmarket(?:ing)?\b|\bbusiness\b|\bcustomers?\b|\brevenue\b|\bprofit|"
               r"(?<![ء-ي])[وف]?(?:ا|ن)?بيع|اسعار|تسويق|عملاء|ارباح|(?<![ء-ي])[وف]?(?:ال)?(?:شركه|مشروع|بيزنس)(?![ء-ي])")
STYLE_RX = {"cinematic": r"سينمائي|cinematic|فيلمي|film look"}   # a style steers families, never the level or the effort
STYLE_FAMILIES = {"cinematic": ["3d-spatial", "light-glow-bloom", "camera-composition-layout", "color-palette-grading", "engines-render-pipeline"]}
LONG_RX = r"طويل|مفصل|شامل|بالتفصيل|\blong(?:form)?\b|detailed|in-depth|comprehensive"
# a subject the request is ABOUT (a research, data or document request on audio is still not a video job)
TOPIC_FAMILIES = {"speech": ["audio-sync-captions", "voice-tts"], "music": ["music-beat-sound"], "motion": ["transitions-cuts", "formats-platforms"],
                  "3d": ["3d-spatial", "engines-render-pipeline"], "reverse": ["software-investigation"]}
TOPIC_RX = {"audio": r"صوت|تفريغ|\basr\b|\bstt\b|speech|whisper|transcri|audio|voice|موسيق|music|podcast|بودكاست",
            "speech": r"صوت|تفريغ|\basr\b|\bstt\b|speech|whisper|transcri|voice|podcast|بودكاست|كلام|نطق",
            "music": r"موسيق|music|\bsong|اغني|\bbeats?\b|ايقاع|نشيد",
            "motion": r"فيديو|video|موشن|motion|انيميشن|animation|مونتاج",
            "3d": r"ثلاثي|\b3d\b|blender|بلندر", "reverse": r"هندسه عكسيه|reverse|ghidra|\bapk\b|electron|الكترون"}
# the user's OWN voice or recording (an ownership form, never the adjective «صوتي» in «تفريغ صوتي» / «بودكاست صوتي»)
OWN_VOICE_RX = (r"بصوتي|فويسي|تسجيلي|(?<![ء-ي])(?:علي|ب|مع|استخدم|خد|حط)\s*صوتي(?![ء-ي])|صوتي (?:المرفق|المسجل|ده|دا|دي)|"
                r"(?:فويس|تسجيل|ريكورد)(?:ات)? (?:بتاعي|المرفق|حقي|تبعي)|عندي (?:فويس|تسجيل)|"
                r"\bmy (?:own )?(?:voice|recording|narration|voice ?over)\b|\bi recorded\b|recorded myself")
# Another person's account or photos ("her account", "bring her photos"): personal data, so L3 and a FULL council,
# and a consent question whose safe default collects nothing from that account. Matched on norm_ar() text.
OTHER_PERSON_RX = (r"((حساب|اكونت|اكاونت|بروفايل|صفحه)\S*\s+(بتاعها|بتاعه|بتاعتها|بتاعهم|بتاعتهم|حقها|حقه|تبعها|تبعه)(?![ء-ي])|"
                   r"(حساب|اكونت|اكاونت|بروفايل|صفحت)(ها|هم)(?![ء-ي])|"
                   r"(هات|جيب|اجمع|جمع|نزل|حمل|اسحب)\S*\s+(\S+\s+){0,2}صور(ها|هم)(?![ء-ي])|"
                   r"صور(ها|هم)\s+من\s+(ال)?(حساب|اكونت|اكاونت|بروفايل|صفحه)|"
                   r"\b(her|his|their|someone'?s|a stranger'?s)\s+(tiktok|instagram|facebook|social|account|profile|photos|pictures)\b|"
                   r"\b(scrape|collect|download|grab)\b.{0,40}\b(her|his|their)\s+(photos|pictures|posts|account|profile)\b)")
# Words of suicide or self-harm, even inside a caption or a joke: a direct check-in comes before any production.
SELF_HARM_RX = (r"(انتحر|انتحار|اموت نفسي|اقتل نفسي|اذي نفسي|اذيه نفسي|ايذاء النفس|"
                r"\bsuicid\w*|\bkill (?:my|him|her|them)sel(?:f|ves)\b|\bself[- ]?harm\w*)")
OWN_FOOTAGE_RX = (r"(فيديو(هات)? (بتاعي|بتاعتي|الخاص(ه)? بي|حقي|تبعي)|فيديوهاتي|مقاطعي|لقطاتي|صوري|تصويري|"
                  r"\bmy (?:own )?(?:footage|videos?|clips?|photos|shots)\b|footage i (?:shot|filmed|recorded))")
SOUND_RX = (r"مونتاج|montage|\breels?\b|ريلز|tiktok|تيك ?توك|shorts|music|موسيق|اغني|\bsongs?\b|نشيد|صوت|voice|audio|podcast|بودكاست|"
            r"narrat|تعليق صوتي|\bbeats?\b|ايقاع")
SILENT_RX = r"صامت|بدون صوت|بلا صوت|من غير صوت|\bsilent\b|no audio|no sound|without (?:sound|audio)|\bmuted?\b"
PLATFORM_RX = {"os:macos": r"mac|ماك|\bios\b|xcode|apple", "engine:android": r"android|apk|اندرويد", "os:windows": r"windows|ويندوز|\.exe|\bexe\b"}
# a push or upload INTENT next to a git target (a bare mention of GitHub or git is research, a question or a topic)
_GIT_TARGET = r"(?:ال)?(?:github|جيت ?هب|\bgit\b|مستودع|ريبو|\brepo\b|\bbranch\b|فرع)"
PUSH_RX = (r"pull request|طلب دمج|\bopen (?:a )?pr\b|\bpr\s*#?\d+|\bgit (?:push|commit)\b|"
           rf"(?:(?<![ء-ي])[وف]?(?:ارفع|رفع|ادفع|انشر)\S*|\b(?:push|commit)(?:ed|es|ing)?\b)(?:\s+\S+){{0,4}}?\s+{_GIT_TARGET}")
# the request already names where the work goes, so the branch question would not change the result
BRANCH_NAMED_RX = (r"(?:new|current|feature|same|separate|existing)\s+branch|\bbranch (?:called|named)\b|\bbranch\s+[\w-]*[/_-][\w./-]*|"
                   r"\b(?:main|master)\b|فرع (?:جديد|حالي|منفصل)|الفرع (?:ال)?(?:حالي|جديد)|نفس الفرع")
MUST_HAVE = [
    ("توقيت الكلمات من صوت المستخدم", r"(كلمات|نص|ترجمه|captions?|subtitles?|words).{0,40}(صوت|فويس|voice|audio)|(صوت|فويس|voice).{0,40}(كلمات|ترجمه|captions?|words)",
     "transcription word timestamps whisper alignment words.json word timing sync"),
    ("نص عربي صحيح RTL", r"عربي|عربيه|arabic|كوفي|ديواني|نستعليق|(?<![ء-ي])[وف]?(?:بال|خط\s+(?:ال)?)(?:رقعه|ثلث|نسخ|مغربي)(?![ء-ي])", "arabic rtl shaping whole word kinetic typography"),
    ("اختبارات آلية", r"اختبار|اختبر(?!ني|نا)|\btests?\b|\btesting\b|unittest|pytest|\btdd\b", "unit tests test suite regression"),   # «اختبرني» = quiz me
    ("رفع على GitHub عبر فرع وطلب دمج", PUSH_RX, "github commit branch pull request git"),
    ("تقرير PDF", r"\bpdf\b", "pdf report generate"),
    ("شخصية متحركة", r"شخصيه|character", "character rig animation blink walk wave"),
    ("مقاس ريلز ومناطق آمنة", r"ريلز|reels?|9:16|تيك ?توك|tiktok|shorts", "vertical 9:16 reels safe area"),
    ("تحليل تطبيق Electron بأدلة", r"electron|asar|الكترون", "electron asar javascript application analysis"),
    ("بناء أصلي نظيف (clean-room) مع بوابة أصالة", r"(ابني|ابن|build|اعمل).{0,40}(مشابه|similar|(?<![ء-ي])زي(?![ء-ي])|\blike\b)|ميزه مشابهه|استفد من (?:افكار|فكره)|استلهم|خد(?:وا)? (?:افكار|فكره)|borrow (?:the )?ideas|inspired by|clean.?room|reimplement|original version|نسخه اصليه", "originality check clean room reimplementation specification"),
    ("محاسبة ومخزون بأرقام صحيحة", r"محاسب|مخزون|inventory|accounting|ledger", "inventory sku stock accounting ledger bookkeeping reconciliation"),
    ("مونتاج وقطع", r"مونتاج|montage", "montage edit cut transitions"),
    ("ترجمة", r"^ترجم|translate", "translation"),
    ("خط مناسب برخصة مؤكدة", None, "arabic font typography font matching fonts license kinetic typography lettering"),
]
_AR = "\u0621-\u064a"
_NOT_FONT_LINE = r"(?!\s+(?:ال)?(?:زمني|انتاج|ساخن|سير|مستقيم|احمر|طول|عرض|الدفاع|النهايه|البدايه|سكه|هاتف|تليفون))"
FONT_RX = (rf"(?<![{_AR}])[وف]?(?:بال|لل|ال|ب|ل)?(?:خطوط|خط|فونتات|فونت)(?![{_AR}]){_NOT_FONT_LINE}|كوفي|ديواني|نستعليق|كاليجراف|تايبو|حروفيه|"
           rf"(?<![{_AR}])[وف]?بال(?:رقعه|ثلث|نسخ|مغربي)(?![{_AR}])|"
           r"\bfonts?\b|typeface|typograph|lettering|calligraph|\bglyphs?\b|شعار(?!\s*(?:ال)?(?:اعلاني|تسويقي|نصي|الحمله|حمله))|لوجو|\blogos?\b|بوستر|\bposters?\b")
ARABIC_ONLY_STYLES = {"kufi", "naskh", "ruqah", "diwani", "thuluth", "maghrebi", "nastaliq"}
STYLE_SKIP = {"arabic", "latin", "licensing", "font_creation"}
MUST_HAVE = [(n, FONT_RX if rx is None else rx, terms) for n, rx, terms in MUST_HAVE]
ARABIC_TERMS = {  # the Arabic-text need means different checks per deliverable
    "image": "arabic shaping harfbuzz glyph ligature font logo poster rtl lettering",
    "document": "arabic writing msa grammar proofread",
    "video": "arabic rtl shaping whole word kinetic typography captions",
    "code": "arabic rtl bidi ui localization shaping",
    "3d": "arabic shaping 3d text extrude glyph",
    "research": "arabic nlp speech recognition asr dialect benchmark",
    "data": "arabic rtl xlsx charts labels",
    "text": "arabic grammar proofread msa",
    "audio": "arabic lyrics pronunciation diacritics",
    "unspecified": "arabic rtl shaping",
}
FONT_TERMS = {"image": "font typography font matching fonts license lettering logo",
              "video": "font typography kinetic typography lettering fonts license"}
CLEANROOM_TERMS = {  # the clean-room need for software means evidence-backed reconstruction, not a prompt-originality check
    "code": "clean room reimplementation specification parity tests reconstruction evidence originality",
    "reverse": "clean room reimplementation specification reconstruction evidence parity originality",
}
# a must-have pick must match through an atom of a family that can meet the need FOR THIS DELIVERABLE; when none does,
# the need is reported as a gap instead of "covered" by an off-target superpower (a video delivery gate is no clean room)
NEED_FAMILIES = {
    "بناء أصلي": {d: {"software-investigation", "app-feature-transfer", "verification-evals", "code-engineering", "atlas-code", "atlas-build",
                     "security-safety", "api-testing"} for d in ("code", "reverse")},
    "محاسبة ومخزون": {d: {"atlas-data", "data-analysis", "strategy-finance", "documents-office", "apps-artifacts", "code-engineering",
                         "atlas-build", "app-feature-transfer"} for d in ("code", "data", "document", "unspecified")},
}
# a superpower built around ONE named platform or product enters a plan, verifies or covers a need only when the request
# names that platform or its domain (a CRUD web app gets no Godot, Shopify, App Store, EVM, GitHub Actions or JEB picks)
NAMED_PLATFORM_GATES = [
    (r"\bgodot\b|gdscript|\bunity\b|phaser", r"لعب|العاب|\bgames?\b|gaming|godot|unity|phaser"),
    (r"\bevm\b|\bnft\b|\bviem\b|solidity|blockchain", r"\bevm\b|\bnfts?\b|ethereum|blockchain|web3|crypto|solidity|بلوك ?تشين|عملات رقميه"),
    (r"shopify", r"shopify|شوبيفاي"),
    (r"app.?store|play store", r"app ?store|play store|متجر (?:ال)?تطبيقات|ابل ستور|جوجل بلاي|app preview"),
    (r"github actions", r"github actions|\bci\b|ci/cd|cicd|\bactions\b|runners?\b|\bpipelines?\b"),
    (r"\bjeb\b|\.jdb2", r"\bjeb\b|jdb2|android|\bapk\b|\bdex\b|اندرويد"),
    (r"mongodb", r"mongo|nosql|مونجو"),
    (r"\bsympy\b|symbolic solving", r"sympy|symbolic|equations?|معادل|\bmath|رياضي|calculus|algebra|جبر|تفاضل"),
    (r"figma", r"figma|فيجما|mock-?ups?|موك ?اب|pixel-?(?:exact|perfect)|design (?:file|handoff)"),
    (r"\bqr\b", r"\bqr\b|باركود|barcode|كيو ار"),
    (r"pipewire", r"pipewire|pulseaudio|linux audio|docker|container"),
    (r"electron", r"electron|الكترون|asar|\bnode\b"),
    (r"native instruction|inspect_macho|hopper", r"native|binary|binaries|\bexe\b|\bdll\b|machine code|assembly|disassembl|x86|\barm64?\b|"
                                                r"firmware|\belf\b|mach-?o|\bipa\b|macos|ثنائي|تنفيذي"),
    (r"\bllms?\b", r"\bllms?\b|\bai\b|ذكاء|نموذج|نماذج|models?\b|agents?\b|وكيل|وكلاء|chat ?bot|بوت|\bbots?\b|\bgpt|claude|prompt|"
                   r"skills?\b|مهار|usip|fusionforge"),
    # an English-only request gets no Arabic-specific superpower ("charts with Arabic labels" is not Arabic-specific)
    (r"^arabic (?!\+)|arabic text\b|\brtl\b(?! mirror)|\(ar/en\)", r"[ء-ي]|arabic|\brtl\b"),
    # superpowers about this skill itself: only for work on the skill, its protocol or its engine
    (r"this skill|capability atlas|skill packager|self-evolution", r"kosif|skills?\b|سكيل|مهار|usip|fusionforge|بروتوكول|protocol|catalog|كتالوج"),
]
TEST_TERMS = {  # the tests need, per deliverable (a motion suite is not a code test suite)
    "code": "test-driven development tdd pytest unittest unit tests code review regression",
    "reverse": "parity tests unit tests regression evidence",
    "video": "motion test suite frame qa golden regression",
    "image": "golden still regression visual test",
}
# Arabic that names the language a tool, library or model handles is not a request for right-to-left output text
ARABIC_TOOL_RX = (r"(?:مكتب|نموذج|نماذج|ادوات|اداه|تفريغ|تعرف|محرك|librar|models?\b|tools?\b|\basr\b|\bstt\b|\bocr\b|\bnlp\b|dataset)"
                  r"\S*(?:\s+\S+){0,2}\s+(?:لل)?(?:عربي|عربيه|العربي|العربيه|arabic)|"
                  r"\barabic\s+(?:asr|stt|ocr|nlp|speech|librar|models?|datasets?|tools?)")
# ... unless the OUTPUT is named Arabic («مقال عربي», «بالعربي», "in Arabic"): then the right-to-left need stays
ARABIC_OUTPUT_RX = (r"(?:مقال|تقرير|نص|نصوص|كلمات|محتوي|بوست|منشور|كتاب|قصيده|عنوان|خطاب|رساله|ايميل|ترجمه|سكريبت|تعليق|كابشن)\S*\s+"
                    r"(?:بال)?عربي|بالعربي|باللغه العربيه|\bin arabic\b|\barabic (?:article|text|copy|captions?|subtitles?|post|report|content)")
FONT_STYLES = {  # request word → query word the atlas understands (its tags are English; its find also matches Arabic)
    "كوفي": "kufi", "ديواني": "diwani", "ثلث": "thuluth", "رقعه": "ruqah", "نسخ": "naskh", "مغربي": "maghrebi",
    "هندسي": "geometric", "يدوي": "handwritten", "فرشاه": "brush", "زخرف": "decorative", "دائري": "rounded", "اطفال": "kids",
    "نستعليق": "nastaliq", "شعار": "logo", "لوجو": "logo", "بوستر": "display", "عناوين": "display", "مجسم": "3d",
    "عريض": "bold", "رفيع": "light", "قديم": "vintage", "حديث": "modern", "متغير": "variable",
    "kufi": "kufi", "naskh": "naskh", "ruqah": "ruqah", "diwani": "diwani", "thuluth": "thuluth", "geometric": "geometric",
    "handwritten": "handwritten", "brush": "brush", "rounded": "rounded", "variable": "variable", "display": "display", "logo": "logo",
    "poster": "display", "kids": "kids", "nastaliq": "nastaliq",
}
# user-owned asset libraries: searched when the request needs them; their files stay on the user's device
ASSET_LIBRARIES = [{
    "id": "telegram-typography-atlas", "trigger": FONT_RX, "index_glob": "data/telegram-typography-catalog-*.json",
    "title_ar": "مكتبة خطوطك من صادرات تيليجرام", "title_en": "Your Telegram typography atlas",
    "where": "ملفات الخطوط نفسها على لابتوبك فقط (ملف المواقع الخاص هناك)؛ هنا فهرس بيانات بلا خطوط. للرندر هنا: خط برخصة مؤكدة من مصدره الرسمي، أو اعمل على اللابتوب عبر Remote Desktop Commander بإذنك.",
    "gate": "رخصة name table تلميح لا تصريح: redistribution_approved=false للكل حتى تُراجع الرخصة الفعلية من مصدرها؛ لا تنسخ حدود حروف خط مملوك.",
    "routes": {"A": "find --license open → أفضل 5 عائلات تناسب النمط → تأكيد الرخصة من المصدر الرسمي",
               "B": "find 15–20 مرشحًا → font-fidelity-lab (تغطية الجملة وGSUB/GPOS) → render-text لوحة مقارنة 16/24/48/96 → اختيار بسبب مكتوب",
               "C": "B + حروف أو شعار أصلي من الصفر مستلهم من فئة الأفكار (unified-draw/creative-paint أو FontForge) + بوابة أصالة"},
    "plan_tools": {"A": ["telegram-typography-atlas"], "B": ["telegram-typography-atlas", "font-fidelity-lab", "render-text"],
                   "C": ["telegram-typography-atlas", "font-fidelity-lab", "render-text", "unified-draw"]},
}]


from hub import AREA_NEEDS_WORDS, TOOL_NEEDS_WORDS  # noqa: E402  (one shared relevance gate with the front door)
BILINGUAL_RX = r"انجليزي|انكليزي|english|\blatin\b|لاتيني|ثنائي اللغه|bilingual"


def _atlas():
    sys.path.insert(0, str(HERE))
    import telegram_typography_atlas as atlas   # same folder; pure Python for tag_text/find
    return atlas


def asset_libraries(task: str) -> list:
    """Libraries the request needs, with live counts read from their public index (no private paths)."""
    low = norm_ar(task.lower())
    out = []
    for lib in ASSET_LIBRARIES:
        if not re.search(lib["trigger"], low):
            continue
        files = sorted(SKILL.glob(lib["index_glob"]))
        if not files:
            continue
        atlas = _atlas()
        idx = files[-1]
        d = jload(idx, {}) or {}
        fonts = d.get("fonts", [])
        lic = collections.Counter(f.get("license_status", "?") for f in fonts)
        styles = [s for s in atlas.tag_text(task) if s not in STYLE_SKIP]
        for w in re.findall(r"[\w]+", low):                 # request words the atlas has no tag for
            s = FONT_STYLES.get(w)
            if s and s not in styles and s not in ("arabic",):
                styles.append(s)
        bilingual = bool(re.search(BILINGUAL_RX, low))
        english_only = bool(re.search(r"انجليزي فقط|english only|لاتيني فقط", low))
        arabic = not english_only and bool(re.search(r"عربي|arabic", low) or set(styles) & ARABIC_ONLY_STYLES
                                           or (re.search(r"[\u0621-\u064a]", low) and not bilingual))
        q = " ".join(styles) or ("arabic" if arabic else "display")
        flags = (" --arabic-only" if arabic else "") + (" --latin" if bilingual or english_only else "")
        open_hits = atlas.find(d, q, 5, True if arabic else None, "open", True, bilingual or english_only) if fonts else []
        rel = idx.relative_to(SKILL).as_posix()
        pre = SKILL.relative_to(REPO).as_posix() if SKILL != REPO else "."
        routes = dict(lib["routes"])
        if not open_hits:
            routes["A"] += " — لا يوجد في مكتبتك خط مفتوح الرخصة لهذا النمط: نزّل خطًا مفتوحًا من مصدره الرسمي، أو اختر الخطة B"
        out.append({"id": lib["id"], "title_ar": lib["title_ar"], "title_en": lib["title_en"], "index": rel,
                    "stats": {"fonts": len(fonts), "arabic": sum(1 for f in fonts if f.get("has_arabic")),
                              "families": (d.get("script_coverage") or {}).get("unique_font_families", 0),
                              "ideas": len(d.get("typography_design_ideas", [])), "license": dict(lic.most_common()),
                              "redistribution_approved": sum(1 for f in fonts if f.get("redistribution_approved"))},
                    "styles_detected": styles, "bilingual": bilingual, "open_license_candidates": [h["family"] for h in open_hits],
                    "command": f'python3 {pre}/scripts/telegram_typography_atlas.py find --index {pre}/{rel} "{q}"{flags} --limit 20',
                    "where": lib["where"], "gate": lib["gate"], "routes": routes, "plan_tools": lib["plan_tools"]})
    return out
VERIFY_TERMS = {
    "video": "verify video delivery gate ffprobe loudness frames qa", "audio": "loudness lufs verify audio qa",
    "code": "tests test suite regression unit coverage test-driven pytest unittest code review evals",
    "reverse": "evidence originality tests golden parity",
    "image": "contrast legibility wcag golden still typography font qa", "3d": "frames verify render check",
    "data": "validation check numbers reconcile agreement anchor totals source tie-out",
    "document": "proofread review check anchor numbers quote citation", "research": "citation fact check sources quote",
    "text": "proofread review language", "unspecified": "verify evidence review check qa",
    "strategy": "assumptions sensitivity scenario risk numbers reconcile pre-mortem",
}
# a verifier must come from a family that can judge this deliverable (a CI cost optimiser never verifies an article)
VERIFY_FAMILIES = {
    "video": {"qa-verification", "formats-platforms", "audio-sync-captions", "music-beat-sound", "transitions-cuts", "engines-render-pipeline",
              "typography-arabic", "color-palette-grading"},
    "audio": {"music-beat-sound", "audio-sync-captions", "voice-tts", "qa-verification"},
    "code": {"code-engineering", "api-testing", "verification-evals", "qa-verification", "security-safety", "atlas-code", "atlas-build", "apps-artifacts"},
    "reverse": {"software-investigation", "verification-evals", "qa-verification", "code-engineering", "app-feature-transfer", "security-safety"},
    "image": {"qa-verification", "typography-arabic", "typography-latin", "brand-logo-identity", "color-palette-grading"},
    "3d": {"3d-spatial", "engines-render-pipeline", "qa-verification", "light-glow-bloom", "texture-material"},
    "data": {"data-analysis", "atlas-data", "charts-data-infographic", "qa-verification"},
    "document": {"writing-humanizer", "documents-office", "atlas-docs", "atlas-craft", "arabic-language", "web-research"},
    "research": {"web-research", "atlas-research", "knowledge-graph", "writing-humanizer", "documents-office"},
    "text": {"writing-humanizer", "arabic-language", "documents-office", "qa-verification"},
    "unspecified": {"qa-verification", "verification-evals"},
    "strategy": {"strategy-finance", "atlas-strategy", "thinking-core", "mental-models", "data-analysis", "qa-verification", "verification-evals"},
}
SOUND_FAMILIES = {"music-beat-sound", "voice-tts"}   # a silent deliverable gets no loudness or voice checks
ARCHETYPES = {
    "video": {"stages": STAGE_ORDER,
              "A": ("محرك المونتاج والقوالب الجاهزة (ffmpeg/Montage Pro)", ["transitions-cuts", "photo-video-footage", "formats-platforms", "video-download", "music-beat-sound", "audio-sync-captions", "runnable-tools"]),
              "B": ("محرك موشن مخصص متزامن مع الكلمات (SVG/HTML)", ["hand-drawn-draw-on", "typography-arabic", "typography-latin", "easing-timing-rhythm", "characters-rigs", "audio-sync-captions", "shapes-morph-geometry", "camera-composition-layout", "runnable-tools"]),
              "C": ("خط سينمائي متعدد المحركات (3D/Remotion/مؤثرات)", ["3d-spatial", "engines-render-pipeline", "light-glow-bloom", "particles-fluids-physics", "color-palette-grading", "texture-material", "characters-rigs", "typography-arabic", "audio-sync-captions"])},
    "code": {"stages": ["understand", "plan", "create", "verify", "deliver"],
             "A": ("إعادة استخدام مكتبة/قالب جاهز وتهيئته", ["apps-artifacts", "atlas-build", "code-engineering"]),
             "B": ("بناء نظيف بمعمارية واختبارات", ["code-engineering", "api-testing", "verification-evals", "security-safety", "apps-artifacts", "atlas-build"]),
             "C": ("بناء + معايير أداء وتكافؤ وأمان وCI", ["code-engineering", "api-testing", "verification-evals", "security-safety", "qa-verification", "atlas-mind", "planning-execution", "atlas-code"])},
    "reverse": {"stages": ["understand", "plan", "create", "verify", "deliver"],
                "A": ("فحص ثابت بـ REA ثم تقرير بنية", ["software-investigation", "runnable-tools"]),
                "B": ("فحص ثابت + بناء أصلي نظيف ببوابة أصالة", ["software-investigation", "code-engineering", "verification-evals", "runnable-tools"]),
                "C": ("فحص ثابت وديناميكي + اختبارات تكافؤ سلوكي", ["software-investigation", "code-engineering", "verification-evals", "qa-verification", "app-feature-transfer", "runnable-tools"])},
    "data": {"stages": ["understand", "plan", "create", "verify", "deliver"],
             "A": ("إعادة حساب مباشرة (DuckDB/pandas) وجدول مطابقة للمصدر", ["data-analysis", "atlas-data", "charts-data-infographic", "documents-office"]),
             "B": ("تحليل استكشافي منضبط + اختبارات مطابقة الأرقام + تقرير", ["data-analysis", "atlas-data", "charts-data-infographic", "qa-verification",
                                                                          "verification-evals", "documents-office"]),
             "C": ("خط بيانات بعقد وبوابات + لوحة تفاعلية بدل التقرير الثابت", ["data-analysis", "atlas-data", "charts-data-infographic", "apps-artifacts",
                                                                             "verification-evals", "planning-execution"])},
    "document": {"stages": ["understand", "plan", "create", "refine", "verify", "deliver"],
                 "A": ("كتابة مباشرة بأسلوب واضح + تدقيق لغوي", ["writing-humanizer", "arabic-language", "documents-office", "atlas-docs"]),
                 "B": ("مصادر + هيكل + كتابة + تدقيق وتوثيق الاقتباسات", ["writing-humanizer", "arabic-language", "documents-office", "web-research",
                                                                      "atlas-research", "qa-verification"]),
                 "C": ("بحث عميق موثق + رسوم ومخططات + تصدير منسق", ["web-research", "atlas-research", "documents-office", "charts-data-infographic",
                                                                    "diagrams-explainers-code", "writing-humanizer"])},
    # a business decision or plan: the deliverable is a defended recommendation, so every plan states assumptions,
    # tests them with numbers and names what would change the answer
    "strategy": {"stages": ["understand", "plan", "create", "verify", "deliver"],
                 "A": ("إطار قرار واضح + أرقام أساسية + توصية واحدة", ["strategy-finance", "atlas-strategy", "thinking-core", "documents-office"]),
                 "B": ("تحليل السوق والمنافسين + سيناريوهات وحساسية الأرقام + خطة تنفيذ بمؤشرات", ["strategy-finance", "atlas-strategy", "mental-models",
                                                                                          "data-analysis", "web-research", "planning-execution", "qa-verification"]),
                 "C": ("نموذج مالي قابل للتعديل + تجربة صغيرة تقيس الفرضية قبل الالتزام", ["data-analysis", "charts-data-infographic", "verification-evals",
                                                                                     "strategy-finance", "apps-artifacts", "planning-execution"])},
    "research": {"stages": ["understand", "plan", "create", "verify", "deliver"],
                 "A": ("بحث موثق المصادر وجدول مقارنة", ["web-research", "atlas-research", "documents-office"]),
                 "B": ("بحث متوازٍ + معايير مقارنة + تحقق من المصادر", ["web-research", "atlas-research", "knowledge-graph", "qa-verification",
                                                                    "verification-evals", "documents-office"]),
                 "C": ("قياس فعلي على عينات (benchmark) ثم تقرير", ["verification-evals", "data-analysis", "runnable-tools", "code-engineering",
                                                                 "web-research", "audio-sync-captions"])},
    "audio": {"stages": STAGE_ORDER,
              "A": ("كتابة/تجهيز مباشر بالقوالب الجاهزة", ["music-beat-sound", "voice-tts", "writing-humanizer", "arabic-language"]),
              "B": ("مسار متوازن: نص + توقيت + ميكس وفحص صوت", ["music-beat-sound", "audio-sync-captions", "voice-tts", "arabic-language", "qa-verification"]),
              "C": ("محرك مختلف: توليد/تحليل إيقاعي ثم مراجعة", ["music-beat-sound", "audio-sync-captions", "ai-generation", "creativity-engine", "verification-evals"])},
    "image": {"stages": ["understand", "plan", "create", "refine", "verify", "deliver"],
              "A": ("خط برخصة مؤكدة + تكوين بسيط واضح", ["typography-arabic", "typography-latin", "brand-logo-identity", "camera-composition-layout", "runnable-tools"]),
              "B": ("تصميم مخصص: مطابقة خطوط + تكوين متجهي + فحص قراءة وتباين", ["typography-arabic", "typography-latin", "brand-logo-identity", "shapes-morph-geometry", "color-palette-grading", "qa-verification", "runnable-tools"]),
              "C": ("حروف أصلية من الصفر + هوية كاملة + موك أب وحركة", ["typography-arabic", "brand-logo-identity", "hand-drawn-draw-on", "shapes-morph-geometry", "texture-material", "light-glow-bloom", "creativity-engine", "easing-timing-rhythm"])},
    # posting or pushing something that already exists: no production stage (no montage, camera or motion picks)
    "publish": {"stages": ["understand", "plan", "refine", "verify", "deliver"],
                "A": ("نشر مباشر بمواصفات المنصة", ["formats-platforms", "documents-office", "atlas-code", "apps-artifacts"]),
                "B": ("فحص مواصفات المنصة ونسخة متوافقة ثم نشر وتحقق بعده", ["formats-platforms", "qa-verification", "verification-evals",
                                                                          "atlas-code", "security-safety", "documents-office"]),
                "C": ("نسخة مخصصة لكل منصة + غلاف وعنوان + متابعة أداء بعد النشر", ["formats-platforms", "story-direction-ideas", "data-analysis",
                                                                                  "charts-data-infographic", "planning-execution", "apps-artifacts"])},
    "_generic": {"stages": STAGE_ORDER,
                 "A": ("المسار الأقصر بأقوى القدرات الجاهزة", []), "B": ("مسار متوازن مع تكامل من مجالات أخرى", []), "C": ("مسار شامل بمراحل ونقاط توقف", [])},
}


# domain affinity per primary deliverable: off-domain clusters are down-weighted, never hidden from the receipt
# keyed on the superpower's majority atom domain AND its plan group (a motion tool filed under domain "build" is still motion)
AFFINITY = {"code": {"motion": 0.4, "reverse": 0.4, "audio": 0.5, "3d": 0.6}, "reverse": {"motion": 0.4, "audio": 0.4},
            "data": {"motion": 0.5, "reverse": 0.4, "audio": 0.5, "3d": 0.5},
            "document": {"motion": 0.5, "reverse": 0.4, "audio": 0.5, "3d": 0.5}, "research": {"motion": 0.5, "reverse": 0.4, "audio": 0.6},
            "text": {"motion": 0.5, "reverse": 0.3, "audio": 0.5},
            "strategy": {"motion": 0.4, "reverse": 0.3, "audio": 0.4, "3d": 0.4, "drawing": 0.5, "images": 0.6, "type": 0.6},
            # nothing named: the motion half of the catalog must not win by size alone
            "unspecified": {"motion": 0.7, "3d": 0.7, "audio": 0.8, "reverse": 0.5},
            # media deliverables: data science, software engineering and binary inspection are off-domain unless the
            # request is about them ("explain transformers in a video" is not a gradient-boosting job)
            "video": {"reverse": 0.3, "data": 0.5, "software": 0.6, "code": 0.6},
            "audio": {"reverse": 0.3, "data": 0.5, "software": 0.6, "code": 0.6},
            "image": {"reverse": 0.3, "docs": 0.5, "code": 0.6, "data": 0.5, "software": 0.6},
            "3d": {"reverse": 0.3, "data": 0.5, "software": 0.6, "code": 0.6}}


HOME_GROUPS = {"code": ["software"], "reverse": ["reverse"], "video": ["motion"], "audio": ["audio"], "3d": ["3d"],
               "image": ["images", "drawing", "type"], "data": ["data"], "strategy": ["thinking"], "document": ["documents"], "research": ["research"], "text": ["documents"]}
MEDIA_TIME_FAMILIES = {"music-beat-sound", "audio-sync-captions", "voice-tts", "transitions-cuts", "video-download"}
MOVING_RX = r"montage|\breels?\b|\bfilm\b|footage|\bvideo\b|transition|camera move|drift|speed ramp"


def affinity(primary: str, sp_domain: str, families, still: bool = False, group: str = None, topics=()) -> float:
    """Down-weight a superpower outside the deliverable's domain. A group the request is about (topics) is never
    penalised, and the superpower's plan group counts as well as its catalog domain."""
    a = AFFINITY.get(primary, {})
    f = a.get("reverse", 1.0) if "software-investigation" in families and "reverse" not in topics else 1.0
    if still and set(families) & MEDIA_TIME_FAMILIES:   # a still image: sound and cutting are off-target
        f = min(f, 0.3)
    if set(families) & {x for t in topics for x in TOPIC_FAMILIES.get(t, [])}:
        return f   # the request is about this medium (speech for an ASR study, 3D for a 3D brief)
    f = min(f, a.get(group, 1.0)) if group else f
    return min(f, a.get(sp_domain, 1.0))


def produces(low: str) -> bool:
    """A production verb or an output format in the (normalised) request, not as part of a how-to question."""
    for m in re.finditer(PRODUCE_RX, low):
        if m.start() == 0 and not re.match(SHORT_INTENTS, low):
            return True
        if not re.search(HOWTO_RX, low[:m.start()]):
            return True
    return False


def story_questions(low: str, level: str) -> list:
    """[(question, suggested_default)] of the story pack (data/question_packs.json, A17) for a story, screenplay or
    scene-sequence request: the core five at L1, all ten at L2/L3, none at L0 or when the pack file is missing."""
    pack = ((jload(QPACKS, {}) or {}).get("packs") or {}).get("story") or {}
    try:
        hit = re.search(pack["match_rx"], low) and not re.search(pack.get("exclude_rx") or r"(?!x)x", low)
    except (KeyError, re.error):
        return []
    n = (pack.get("levels") or {}).get(level, 0)
    if not hit or not n:
        return []
    scenes = re.search(r"(\d+)\s*(مشاهد|مشهد|scenes?|ثانيه|ثواني|دقيقه|دقائق|sec\w*|min\w*)", low)
    out = []
    for q in (pack.get("questions") or [])[:n]:
        d = q["suggested_default"]
        if q.get("id") == "scenes" and scenes:
            d = f"{scenes.group(1)} {scenes.group(2)} (من طلبك)"
        out.append((q["question"], d))
    return out


def analyse(task: str) -> dict:
    low = norm_ar(task.lower())
    deliver = [k for k, rx in DELIVERABLES if re.search(rx, low)]
    if (re.search(FONT_RX, low) and re.search(r"(?<![ء-ي])(?:اختار|اختر|رشح|اقترح|ترشح)|\b(?:pick|choose|suggest)\b", low)
            and not re.search(r"ابني|برمج|اكتب كود|\bbuild\b|\bcode\b", low)):
        deliver = ["image"] + [d for d in deliver if d not in ("code", "image")]
    if not deliver and re.search(FONT_RX, low):
        deliver = ["image"]   # choosing or designing type is a visual deliverable
    if re.search(r"cover letters?|\bresumes?\b|\bcv\b|سيره ذاتيه|خطاب (?:تقديم|تحفيزي)", low):
        deliver = ["document"] + [d for d in deliver if d != "document"]   # a cover letter for a data job is a letter
    if re.match(RESEARCH_LEAD_RX, low.strip()) and not re.search(NEW_WORK_RX, low) and (not deliver or deliver[0] == "code"):
        deliver = ["research"] + [d for d in deliver if d != "research"]   # "find the best GitHub repos for…" is a search
    if "document" in deliver and re.search(WRITTEN_PIECE_RX, low):
        deliver = ["document"] + [d for d in deliver if d != "document"]   # a sales email is a letter, not a dataset
    if "strategy" in deliver and re.search(DECISION_LEAD_RX, low) and re.search(BUSINESS_RX, low):
        deliver = ["strategy"] + [d for d in deliver if d != "strategy"]   # "should we build an app or sell on Shopify?"
    named = list(deliver)       # deliverables the request names outright (an explain-question about git stays L0)
    meta = re.search(META_CODE_RX, low) or (re.search(META_WEAK_RX, low) and re.search(SOFTWARE_CTX_RX, low))
    if "code" not in deliver and meta and not (named and named[0] in ("research", "document")):
        deliver.append("code")  # protocol / engine / skill / GitHub work: software, but after any stronger deliverable
                                # (an article or a comparison ABOUT GitHub is not a software job)
    numbers = re.findall(r"\d+(?:[.,]\d+)?\s*(?:ثانيه|ثواني|ث|دقيقه|دقائق|sec|min|fps|%|k)?", task)
    aspects = re.findall(r"\b(?:9:16|16:9|1:1|4:5|21:9|4:3)\b", task)
    paths = re.findall(r"[\w./\\:-]+\.(?:mp4|mov|wav|mp3|m4a|png|jpg|jpeg|pdf|docx|xlsx|csv|json|py|js|ts|blend|glb|exe|dll|apk|asar)\b", task, re.I)
    existing = [p for p in paths if Path(p).expanduser().exists()]
    ntok = len(tokens(task))
    ambition = "max" if re.search(MAX_RX, low) else ("fast" if re.search(FAST_RX, low) else "balanced")
    style = [k for k, rx in STYLE_RX.items() if re.search(rx, low)]
    s = low.strip()
    heavy = set(named) & {"video", "code", "reverse", "3d"}
    publish = bool(re.search(PUBLISH_RX, low) and re.search(PUBLISH_DEST_RX, low) and re.search(PUBLISH_OBJ_RX, low)
                   and not re.search(NEW_WORK_RX, low))
    if (re.search(SHORT_INTENTS, s) and not paths and ntok <= 14 and not produces(s) and not re.search(COMPOUND_RX, s)
            and (not heavy or (re.search(DEFINE_RX, s) and not re.search(EXISTING_OBJ_RX, s)))):
        level = "L0"   # a question, explanation or definition (also "what does API mean?" / «ما معنى موشن جرافيك؟»)
    elif ambition == "max":
        level = "L3"
    elif publish:
        level = "L1"   # posting or pushing something that exists: delivery, not new production
    elif not paths and ntok <= 8 and not set(deliver) & {"video", "code", "reverse", "3d", "data"} and not re.search(LONG_RX, low):
        level = "L1"
    else:
        level = "L2"
    if level == "L0":
        deliver = named
    primary = deliver[0] if deliver else ("text" if level == "L0" else "unspecified")
    own = {"voice": bool(re.search(OWN_VOICE_RX, low)), "footage": bool(re.search(OWN_FOOTAGE_RX, low))}
    if (own["voice"] or own["footage"]) and level in ("L0", "L1") and not publish:
        level = "L2"   # the user's own files are involved
    other = bool(re.search(OTHER_PERSON_RX, low))
    harm = bool(re.search(SELF_HARM_RX, low))
    if other and level in ("L1", "L2"):
        level = "L3"   # another person's account or photos: personal data (FULL council, safe default)
    sensitive = [k for k, v in (("personal_data", other), ("self_harm", harm)) if v]
    topics = [g for g, rx in TOPIC_RX.items() if re.search(rx, low)]
    musts = []
    for n, rx, terms in MUST_HAVE:
        if not re.search(rx, low):
            continue
        if n.startswith("نص عربي"):
            if re.search(ARABIC_TOOL_RX, low) and not re.search(FONT_RX, low) and not re.search(ARABIC_OUTPUT_RX, low):
                continue   # Arabic is what the library or model handles, not right-to-left output text
            terms = ARABIC_TERMS.get(primary, terms)
            if primary in ("document", "text") and re.search(r"docx|\bpdf\b|وورد|\bword\b|عرض تقديمي|slides|pptx", low):
                terms += " rtl docx pdf shaping"   # a file format: right-to-left layout matters, not only the language
        elif n.startswith("اختبارات"):
            terms = TEST_TERMS.get(primary, TEST_TERMS["code"])
        elif n.startswith("بناء أصلي"):
            terms = CLEANROOM_TERMS.get(primary, terms)
        elif n.startswith("خط مناسب"):   # a logo needs font matching, a lyric video kinetic type; Arabic only when asked
            terms = FONT_TERMS.get(primary, FONT_TERMS["image"]) + (" arabic" if re.search(r"[ء-ي]|arabic", low) else "")
        elif n.startswith("محاسبة") and (primary == "reverse" or "reverse" in topics):
            continue   # an artefact inventory of a binary is not bookkeeping
        musts.append({"need": n, "terms": terms})
    if ("reverse" in deliver and re.search(r"rebuild|re-build|اعد بناء|اعاده بناء|ابني نسخه|اعمل نسخه", low)
            and not any(m["need"].startswith("بناء أصلي") for m in musts)):
        n, _rx, terms = next(x for x in MUST_HAVE if x[0].startswith("بناء أصلي"))
        musts.append({"need": n, "terms": CLEANROOM_TERMS.get(primary, terms)})
    if re.search(FONT_RX, low) and re.search(BILINGUAL_RX, low):
        musts.append({"need": "زوج خطوط يغطي العربية واللاتينية", "terms": "arabic latin font pairing bilingual typography type pairings"})
    platforms = [k for k, rx in PLATFORM_RX.items() if re.search(rx, low)]
    questions, qdefaults = [], []
    if primary == "video" and not aspects and not publish:   # a named platform already fixes the spec of a post
        questions.append("المقاس والمنصة (9:16 ريلز؟ 16:9 يوتيوب؟)")
        qdefaults.append("9:16 ريلز" if re.search(r"ريلز|reels?|تيك ?توك|tiktok|shorts", low) else "16:9 يوتيوب")
    if (own["voice"] or own["footage"] or primary in ("reverse",)) and not existing:
        questions.append("أين الملف المصدر؟ (رفع في الجلسة، مسار على جهازك عبر Remote Desktop Commander بإذنك، أو رابط)")
        qdefaults.append("ارفعه في الجلسة")
    if any(m["need"].startswith("رفع على GitHub") for m in musts) and not re.search(BRANCH_NAMED_RX, low):
        questions.append("إلى أي فرع يُرفع العمل؟ (فرع جديد + طلب دمج، أم الفرع الحالي)")
        qdefaults.append("فرع جديد + طلب دمج؛ لا دفع إلى main بلا إذن صريح")
    for q_, d_ in story_questions(low, level):
        questions.append(q_)
        qdefaults.append(d_)
    if harm:   # first: safety outranks every production question
        questions.insert(0, "سلامة: في الطلب لفظ انتحار أو إيذاء للنفس، هل الشخص بخير الآن؟")
        qdefaults.insert(0, "اطمئنان مباشر منك أولًا، وأرقام دعم بلده بعد التحقق منها، قبل أي إنتاج")
    if other:
        questions.append("صور الشخص وموافقته: ما علاقتك به، وهل وافق؟ الصور تأتي منك أو منه بموافقته، لا من حسابه")
        qdefaults.append("لا جمع من حسابه؛ نسخة بلا صوره حتى تصل صور بموافقته؛ لا نشر")
    if level == "L0":
        questions, qdefaults, musts = [], [], []   # L0 gets no plans, no questions and no must-haves
    still = primary == "image" and not set(deliver) & {"video", "audio"}
    # silent only on an explicit cue, or when nothing in the request carries sound (own footage, a montage or reel does)
    silent = bool(re.search(SILENT_RX, low)) or not (own["voice"] or own["footage"] or set(deliver) & {"audio"} or "audio" in topics
                                                     or re.search(SOUND_RX, low))
    return {"request": task, "level": level, "deliverables": deliver or [primary], "primary": primary, "ambition": ambition, "still": still,
            "style": style, "topics": topics, "silent": silent, "intent": "publish" if publish else "produce",
            "sensitive": sensitive,
            "constraints": {"numbers": [n.strip() for n in numbers if n.strip()], "aspects": aspects, "own_assets": own, "platforms_mentioned": platforms},
            "files_mentioned": paths, "files_found": existing, "must_haves": musts, "open_questions": questions,
            "questions": [{"question": q_, "suggested_default": d_} for q_, d_ in zip(questions, qdefaults)],
            "claude_must_answer": ["ماذا يريد حرفيًا؟", "ما النتيجة النهائية؟", "ما المشكلة الأساسية؟", "المتطلبات الصريحة والضمنية",
                                   "مستوى الجودة والجمهور", "القيود: وقت/تكلفة/أجهزة/صلاحيات/ترخيص", "معايير نجاح قابلة للقياس", "طريقة أذكى من وصف المستخدم؟"]}


# ------------------------------------------------------------------ ranking
_DF_CACHE = {}


def build_df(records):
    """Document frequencies and per-record term counts (cached per catalog content, so repeated briefs are fast)."""
    key = hashlib.sha256("\x00".join(r["id"] + "\x01" + r["text"] for r in records).encode("utf-8")).hexdigest()
    if key not in _DF_CACHE:
        df = collections.Counter()
        toks = []
        for r in records:
            t = collections.Counter(tokens(r["text"]))
            toks.append(t)
            for w in t:
                df[w] += 1
        _DF_CACHE.clear()
        _DF_CACHE[key] = (df, toks, [set(tokens(r["name_en"] + " " + r["name_ar"])) for r in records])
    df, toks, names = _DF_CACHE[key]
    for r, nm in zip(records, names):
        r["_name_tokens"] = nm
    return df, toks


PROCESS_TERMS = {"github", "commit", "branch", "git", "test", "testing", "tests", "pytest", "unittest", "اختبار", "اختبارات", "اختبر"}
QUALIFIER_TERMS = {"arabic"}   # the language of the output: the right-to-left must-have routes it, in the ranking it only qualifies


SUBJECT_RX = r"(?:^|\s)(?:عن|حول|about|on the topic of)\s+(.+)$"


def concept_weights(groups, an: dict = None) -> list:
    """A process step the must-have layer already routes (tests, a GitHub push) is a qualifier in the general ranking,
    not the subject: without this every GitHub-Actions or motion-test superpower outranks the actual work. For a text
    deliverable, what the text is ABOUT is content, not a capability need ("an article about AI" needs writing tools,
    not LLM-ops tools)."""
    subject = set()
    if an and an.get("primary") in ("document", "text"):
        m = re.search(SUBJECT_RX, norm_ar(an.get("request", "").lower()))
        subject = set(tokens(m.group(1))) if m else set()
    style = {w for w in (g[0] for g in groups if g) if any(re.search(rx, w) for rx in STYLE_RX.values())}
    out = []
    for g in groups:
        if set(g) & PROCESS_TERMS:
            out.append(0.35)
        elif g and g[0] in subject:
            out.append(0.3)
        elif g and (g[0] in style or set(g) & QUALIFIER_TERMS):
            out.append(0.5)
        else:
            out.append(1.0)
    return out


def score_records(records, toks, df, words, detail=False, weights=None):
    """Relevance of every record. `words` is a flat list of terms or a list of concepts (lists of interchangeable
    terms): a concept scores once per record, by its best term, so a word and its alias are not counted twice.
    `weights` scales each concept. detail=True returns (score, {concept index: score}) per record."""
    groups = [list(g) if isinstance(g, (list, tuple)) else [g] for g in words]
    weights = list(weights) if weights else [1.0] * len(groups)
    n = len(records)
    idf = {w: math.log(1 + n / (1 + df.get(w, 0))) for g in groups for w in g}
    prefixed = {w: [k for k in df if k != w and k.startswith(w)] for g in groups for w in g if len(w) >= 4}
    out = []
    for r, t in zip(records, toks):
        name = r.get("_name_tokens")
        if name is None:
            name = set(tokens(r["name_en"] + " " + r["name_ar"]))
        s, parts = 0.0, {}
        for gi, g in enumerate(groups):
            best = 0.0
            for w in g:
                tf = t.get(w, 0)
                if not tf and w in prefixed:
                    tf = sum(t.get(k, 0) for k in prefixed[w])
                if tf:
                    best = max(best, (1 + math.log(1 + tf)) * idf[w] * (2.2 if w in name else 1.0))
            if best:
                best *= weights[gi]
                s += best
                parts[gi] = best
        out.append((s, parts) if detail else s)
    return out


def local_badge(atom, pres) -> str:
    """Badge as it stands HERE: requirements present on this machine and proof inside this checkout."""
    req = atom.get("requires") or []
    if any(str(k).startswith("key:") and pres.get(k) != "present" for k in req):
        return "🔑"
    if any(pres.get(k) == "missing" for k in req if not str(k).startswith("key:")):
        return "📦"
    st, scope = atom.get("status"), atom.get("proof_scope")
    if st == "proven":
        return "✅" if scope == "repo" else "🟢"
    if st == "ready":
        return "🟢"
    if st in ("install",):
        return "📦"
    if st == "key":
        return "🔑"
    if st == "idea":
        return "💡"
    return "📄"


GROUP_DELIVERABLE = {"software": "code", "thinking": "strategy", "data": "data", "documents": "document", "research": "research"}


def infer_primary(records, scores, fam2group, top: int = 40):
    """When the request names no deliverable, let the catalog vote: the best-matching powers' groups, media and support
    groups left out (no media word was named, or a deliverable would have matched). Returns (deliverable, votes) or
    (None, votes) when no group leads clearly. The motion half of the catalog never wins by size: only the top
    matches vote, each by its score."""
    votes = collections.Counter()
    for sc, r in sorted(((sc, r) for r, sc in zip(records, scores) if sc > 0), key=lambda x: (-x[0], x[1]["id"]))[:top]:
        g = fam2group.get(r.get("family"), "misc")
        if g in GROUP_DELIVERABLE:
            votes[GROUP_DELIVERABLE[g]] += sc
    ranked = votes.most_common(2)
    if not ranked:
        return None, {}
    lead = ranked[0][1] / (ranked[1][1] if len(ranked) > 1 and ranked[1][1] else 1e-9)
    rounded = {k: round(v, 1) for k, v in votes.items()}
    return (ranked[0][0] if lead >= 1.25 else None), rounded


def build_brief(task: str, details=False, terms: str = "") -> dict:
    t0 = time.time()
    scan = scan_catalog()
    records, receipt = scan["records"], scan["receipt"]
    fresh = freshness(records)
    an = analyse(task)
    df, toks = build_df(records)
    cq = concepts(task, df, terms)
    q = expand(task, df, terms)
    detail = score_records(records, toks, df, cq, detail=True, weights=concept_weights(cq, an))
    scores = [d[0] for d in detail]
    parts_of = {r["id"]: d[1] for r, d in zip(records, detail)}
    cw = concept_weights(cq, an)
    cmax = [max((d[1].get(gi, 0.0) for d in detail), default=0.0) for gi in range(len(cq))]   # best score per concept
    by_id = {r["id"]: (r, s) for r, s in zip(records, scores)}
    reg, pres = requirement_presence()
    tools = tool_registry()
    pid2tool = {t.get("power_id"): t for t in tools.values() if t.get("power_id")}
    fam2group = fam_to_group()
    # protocol / engine / workflow words without a software context are ambiguous on purpose (META_WEAK_RX): no vote
    if an["primary"] == "unspecified" and an["level"] != "L0" and not re.search(META_WEAK_RX, norm_ar(task.lower())):
        inferred, votes = infer_primary(records, scores, fam2group)
        an["primary_votes"] = votes
        if inferred:
            an["primary"], an["deliverables"], an["primary_inferred"] = inferred, [inferred], True

    def plan_group(fams: dict, members) -> str:
        c = collections.Counter()
        for m in members:
            a = by_id.get(m["id"], ({}, 0))[0]
            if a.get("family") == "runnable-tools" and a.get("id") in pid2tool:
                c[TOOL_AREA_GROUP.get(pid2tool[a["id"]].get("area"), "agents")] += 1
            elif a.get("family"):
                c[PLAN_GROUP.get(a["family"], fam2group.get(a["family"], "misc"))] += 1
        return c.most_common(1)[0][0] if c else "misc"

    relevant = sorted(((s, r) for r, s in zip(records, scores) if s > 0), key=lambda x: (-x[0], x[1]["id"]))
    sp = jload(SP, {"items": []})
    mind = jload(MIND, {}) or {}
    stage_of = {k: v.get("stage") for k, v in (mind.get("superpowers") or {}).items()}
    own_voice = an["constraints"]["own_assets"]["voice"]
    mentioned_platforms = set(an["constraints"]["platforms_mentioned"])
    asked_low = norm_ar(f"{task} {terms}".lower())
    excluded = []
    sp_rows = []
    for s in sp.get("items", []):
        ms = [(by_id[m["id"]][0], by_id[m["id"]][1]) for m in s["pipeline"] if m["id"] in by_id]
        rel = sorted((sc for _r, sc in ms), reverse=True)
        if not rel or rel[0] <= 0:
            continue
        depth = rel[0] + 0.25 * sum(rel[1:4])            # best atom + a quarter of the next three
        best_c = [max(parts_of[a["id"]].get(gi, 0.0) for a, _ in ms) for gi in range(len(cq))]
        cover = sum(best_c)                              # each concept once, by its best atom
        n_conc = sum(1 for gi in range(len(cq)) if best_c[gi] > 0 and cw[gi] >= 0.5)   # request concepts it matches
        share_c = sum(cw[gi] * best_c[gi] / cmax[gi] for gi in range(len(cq)) if cmax[gi]) / (sum(cw[gi] for gi in range(len(cq)) if cmax[gi]) or 1)
        fit = (depth + cover) / 2 / (1 + 0.15 * math.log(max(1, len(ms))))   # many atoms do not buy rank
        fit *= 0.5 + 0.5 * share_c                       # how much of the request this superpower covers
        fam_count = collections.Counter(a["family"] for a, _ in ms)
        if own_voice and (fam_count.get("voice-tts", 0) >= 0.5 * len(ms) or re.search(r"\btts\b|text.to.speech|voice clon|elevenlabs|voice costume", s["name_en"].lower())):
            excluded.append({"id": s["id"], "name": s["name_en"], "reason": "يستبدل صوت المستخدم (TTS/استنساخ) والطلب على صوته هو"})
            continue
        plat = {k for a, _ in ms for k in a.get("requires") or [] if k in PLATFORM_RX}
        if plat and not plat & mentioned_platforms:
            fit *= 0.3
        gated = any(re.search(nrx, s["name_en"].lower()) and not re.search(rrx, asked_low) for nrx, rrx in NAMED_PLATFORM_GATES)
        if gated:
            fit *= 0.3   # built around a platform the request does not name
        dom = collections.Counter(a.get("domain") or "motion" for a, _ in ms).most_common(1)[0][0]
        grp = plan_group(s.get("families", {}), s["pipeline"])
        fit *= affinity(an["primary"], dom, fam_count, an["still"], grp, an["topics"])
        hits = sorted(((a, sc) for a, sc in ms if sc > 0), key=lambda x: -x[1])
        self_tools = [pid2tool.get(a["id"]) for a, _ in hits[:2]]
        if self_tools and an["primary"] not in ("research", "unspecified") and all(
                t and (META_TOOL_RX.match(t["id"]) or "self-discovery" in t.get("families", [])) for t in self_tools):
            fit *= 0.3   # what matched is the skill's own maintenance/self-discovery tooling, not the user's job
        if an["still"] and re.search(MOVING_RX, " ".join(a["name_en"] for a, _ in hits[:2]).lower()):
            fit *= 0.5   # a still image: what matched is about moving pictures
        badges = [local_badge(a, pres) for a, _ in (hits or ms)]
        lb = min(badges, key=LOCAL_RANK.index) if badges else "📄"
        ready_local = sum(1 for a, _ in ms if local_badge(a, pres) in ("✅", "🟢"))
        sp_rows.append({"id": s["id"], "name_ar": s["name_ar"], "name_en": s["name_en"], "group": grp, "domain": dom,
                        "families": list(fam_count), "stage": stage_of.get(s["id"], "create"), "size": s["size"], "catalog_best": s["best"],
                        "local_badge": lb, "ready_local": ready_local, "requires": s.get("requires", []), "links": [l["id"] for l in s.get("links", [])],
                        "hit_requires": sorted({str(k) for a, _ in hits[:2] for k in a.get("requires") or []}),   # what the best matches need
                        "fit_raw": fit, "hits": [a["id"] for a, _ in hits], "contains": [a["name_en"] for a, _ in hits[:3]],
                        "badge_mix_local": dict(collections.Counter(badges)), "gated": gated, "n_concepts": n_conc})
    sp_rows.sort(key=lambda x: -x["fit_raw"])
    maxfit = max([x["fit_raw"] for x in sp_rows] or [1.0])
    gsc = collections.Counter()
    for x in sp_rows[:80]:
        gsc[x["group"]] += x["fit_raw"]
    # core groups: the deliverable's own group(s) plus the two strongest groups that are not off-domain for it
    pen = AFFINITY.get(an["primary"], {})
    eligible = [g for g, _ in gsc.most_common() if not (pen.get(g, 1.0) < 1.0 and g not in an["topics"])]
    top_groups = list(dict.fromkeys(HOME_GROUPS.get(an["primary"], []) + eligible[:2]))

    n_req = sum(1 for w_ in cw if w_ >= 0.5)
    home = {g for d in an["deliverables"] for g in HOME_GROUPS.get(d, [])} | set(an["topics"])
    pen_ok = lambda g: pen.get(g, 1.0) >= 1.0 or g in home   # a cross-domain integration never comes from an off-domain group

    # must-have layer: each need gets its own sub-ranking and at least one superpower
    must_cov = []
    must_ids = set()
    top_atom = max([s for s, _ in relevant[:1]] or [1.0])
    sp_by_id = {x["id"]: x for x in sp_rows}
    atom2sp = {m["id"]: s["id"] for s in sp.get("items", []) for m in s["pipeline"]}
    media_words = set(an["topics"]) | set(an["deliverables"])

    def off_need(row) -> bool:
        """A must-have pick from the wrong sense of the need's words: reverse-engineering tools outside a reverse job,
        motion/audio/3D suites for a code, data, document or research deliverable that names no such medium."""
        if "software-investigation" in row["families"] and an["primary"] != "reverse" and "reverse" not in an["topics"]:
            return True
        return row["group"] in ("motion", "audio", "3d") and an["primary"] in ("code", "reverse", "data", "strategy", "document", "research", "text", "unspecified") \
            and row["group"] not in media_words and not (row["group"] == "motion" and "video" in media_words)

    for need in an["must_haves"]:
        w = concepts(need["terms"], df)
        sub = score_records(records, toks, df, w)
        allowed = next((v.get(an["primary"]) for k, v in NEED_FAMILIES.items() if need["need"].startswith(k)), None)
        best_atoms = []
        for sc, r in sorted(((sc, r) for r, sc in zip(records, sub) if sc > 0), key=lambda x: -x[0]):
            sid = atom2sp.get(r["id"])
            if allowed and r.get("family") not in allowed:
                continue   # this family cannot meet the need for this deliverable
            if sid in sp_by_id and (off_need(sp_by_id[sid]) or sp_by_id[sid]["gated"]):
                continue
            best_atoms.append((sc, r))
            if len(best_atoms) >= 16:
                break
        per = collections.defaultdict(list)
        for sc, r in best_atoms:
            sid = atom2sp.get(r["id"])
            if sid and sid in sp_by_id:
                row = sp_by_id[sid]
                ctx = by_id[r["id"]][1] / top_atom   # how much this atom also matches the whole request
                per[sid].append(sc * (1 + ctx) * affinity(an["primary"], row["domain"], row["families"], an["still"], row["group"], an["topics"]))
        agg = collections.Counter()
        for sid, v in per.items():   # normalised like fit: a superpower with many weak atoms does not outvote one strong match
            v.sort(reverse=True)
            agg[sid] = v[0] + 0.25 * sum(v[1:4])
        ranked_need = agg.most_common(2)
        pick = [ranked_need[0][0]] if ranked_need else []
        if len(ranked_need) > 1 and ranked_need[1][1] >= 0.75 * ranked_need[0][1] and sp_by_id[ranked_need[1][0]]["fit_raw"] >= MIN_FIT * maxfit:
            pick.append(ranked_need[1][0])   # a second pick must also fit the request, not only the need's words
        top_sid = atom2sp.get(best_atoms[0][1]["id"]) if best_atoms else None
        if pick and top_sid in sp_by_id and top_sid not in pick and agg[top_sid] >= 0.75 * ranked_need[0][1]:
            pick.append(top_sid)   # the need's single best-matching atom keeps its superpower in, even beside a broader pick
        must_ids.update(pick)
        must_cov.append({"need": need["need"], "superpowers": pick, "atoms": [r["id"] for _, r in best_atoms[:4]],
                         "status": "covered" if pick else "gap", "local_badges": [sp_by_id[p]["local_badge"] for p in pick]})
    # scoring
    short = sp_rows[:60] + [sp_by_id[i] for i in must_ids if i not in {x["id"] for x in sp_rows[:60]}]
    short_ids = {x["id"] for x in short}
    for x in short:
        integ = len([l for l in x["links"] if l in short_ids])
        req_used = x.get("hit_requires") or x["requires"]   # cost of the atoms that match, not of every member
        miss = [k for k in req_used if pres.get(k) == "missing"]
        keys = [k for k in req_used if str(k).startswith("key:") and pres.get(k) != "present"]
        share = x["fit_raw"] / maxfit
        strong_outside = (x["group"] not in top_groups and share >= 0.4 and pen_ok(x["group"]) and pen_ok(x["domain"])
                          and x.get("n_concepts", 0) >= min(2, n_req))   # one homonym hit is not an integration
        g = min(1.0, share / MIN_FIT)   # below the fit floor, readiness and links cannot lift an off-target pick up the shortlist
        sc = {"fit": share, "integration": min(1.0, integ / 3) * g,   # links cannot outrank relevance
              "feasibility": x["ready_local"] / max(1, x["size"]) * g,
              "evidence": LOCAL_EVIDENCE.get(x["local_badge"], 0.2) * g, "cost": (1.0 - min(1.0, 0.25 * len(miss) + 0.5 * len(keys))) * g,
              "creativity": share if strong_outside else 0.3 * share}   # scaled by fit: an off-target pick is not "creative"
        x["score"] = round(sum(WEIGHTS[k] * v for k, v in sc.items()), 1)
        x["score_parts"] = {k: round(WEIGHTS[k] * v, 1) for k, v in sc.items()}
        x["fit_share"] = round(share, 3)
        x["missing"], x["needs_key"] = miss, keys
        x["role"] = "must-have" if x["id"] in must_ids else ("core" if x["group"] in top_groups and share >= MIN_FIT
                                                              else ("cross-domain" if strong_outside else "peripheral"))
    short.sort(key=lambda x: (x["role"] != "must-have", -x["score"]))
    # verifiers by deliverable: normalised per superpower (best atom + 0.25 x next three), from a family that can judge
    # this deliverable, keys checked per matched atom, no sound checks for a silent deliverable, no off-domain checker
    # and weighted by how much the checker also matches THIS request (two data requests do not get the same verifiers)
    arabic_out = any(m["need"].startswith("نص عربي") for m in an["must_haves"]) or bool(
        an["primary"] in ("document", "text") and re.search(r"[ء-ي]", task))
    vterms = VERIFY_TERMS.get(an["primary"], VERIFY_TERMS["unspecified"]) + (" arabic" if arabic_out and an["primary"] == "image" else "")
    vt = concepts(vterms, df)
    vsc = score_records(records, toks, df, vt)
    vfam = set(VERIFY_FAMILIES.get(an["primary"], VERIFY_FAMILIES["unspecified"]))
    if not arabic_out:
        vfam -= {"typography-arabic", "arabic-language"}   # an English logo or report gets no Arabic-typography check
    sp_items = {y["id"]: y for y in sp.get("items", [])}

    def name_gated(name: str) -> bool:
        return any(re.search(nrx, name.lower()) and not re.search(rrx, asked_low) for nrx, rrx in NAMED_PLATFORM_GATES)
    meta_cache = {}

    def sp_meta(sid):
        if sid in sp_by_id:
            b_ = sp_by_id[sid]
            return b_["domain"], b_["families"], b_["group"]
        if sid not in meta_cache:
            y = sp_items[sid]
            mem = [by_id[m["id"]][0] for m in y["pipeline"] if m["id"] in by_id]
            dom_ = collections.Counter(a.get("domain") or "motion" for a in mem).most_common(1)[0][0] if mem else "motion"
            meta_cache[sid] = (dom_, list(y.get("families", {})), plan_group(y.get("families", {}), y["pipeline"]))
        return meta_cache[sid]

    per_sp = collections.defaultdict(list)
    v_best, v_sound = {}, set()
    for r, sc in zip(records, vsc):
        sid = atom2sp.get(r["id"])
        if sc <= 0 or not sid or r.get("family") not in vfam:
            continue
        if any(str(k).startswith("key:") and pres.get(k) != "present" for k in r.get("requires") or []):
            continue
        if an["silent"] and (r.get("family") in SOUND_FAMILIES or re.search(r"loudness|\blufs\b|\bsound\b|\baudio\b", r["name_en"].lower())):
            continue
        dom_, fams_, grp_ = sp_meta(sid)
        aff = affinity(an["primary"], dom_, fams_, an["still"], grp_, an["topics"])
        if aff < 0.6 or name_gated(sp_items[sid]["name_en"]):
            continue
        ctx = by_id[r["id"]][1] / top_atom                                     # this atom also matches the request
        fs = sp_by_id[sid]["fit_raw"] / maxfit if sid in sp_by_id else 0.0     # its superpower fits the request
        v_ = sc * aff * (1 + ctx + fs)
        per_sp[sid].append(v_)
        if v_ > v_best.get(sid, (0, "", ""))[0]:
            v_best[sid] = (v_, r["name_en"], r.get("family"))
        if re.search(r"loudness|\blufs\b|true.?peak", sp_items[sid]["name_en"].lower()):
            v_sound.add(sid)   # a dedicated sound check (not a gate that also reads LUFS)
    vagg = {}
    for sid, v in per_sp.items():
        v.sort(reverse=True)
        vagg[sid] = v[0] + 0.25 * sum(v[1:4])
    v_order = sorted(vagg, key=lambda k: (-vagg[k], k))
    snd = [sid for sid in v_order if sid in v_sound]
    if not an["silent"] and an["primary"] in ("video", "audio") and snd and snd[0] not in v_order[:2]:
        v_order.remove(snd[0])
        v_order.insert(1, snd[0])   # a montage, reel or voice track carries sound: the balanced plan checks its loudness
    verifiers = []
    for sid in v_order[:4]:   # A uses 1, B the first 2, C the first + 3rd/4th (another method)
        y = sp_items[sid]
        dom_, fams_, grp_ = sp_meta(sid)
        s = sp_by_id.get(sid) or {"id": y["id"], "name_ar": y["name_ar"], "name_en": y["name_en"], "group": grp_, "domain": dom_, "stage": "verify",
                                  "size": y["size"], "catalog_best": y["best"], "local_badge": "📄", "ready_local": 0, "requires": y.get("requires", []),
                                  "links": [], "fit_raw": 0, "hits": [], "contains": [], "families": fams_, "score": 0,
                                  "role": "verifier", "missing": [], "needs_key": []}
        s = dict(s)
        s["stage"], s["role"], s["verify_score"] = "verify", "verifier", round(vagg[sid], 2)
        s["contains"] = [v_best[sid][1]] + [c for c in s.get("contains", []) if c != v_best[sid][1]][:1]
        s["via_family"] = v_best[sid][2]
        verifiers.append(s)
    # complements: linked to a top pick, relevant themselves, same or adjacent stage
    comp = []
    for x in short[:8]:
        for l in x["links"]:
            y = sp_by_id.get(l)
            if y and l not in short_ids and y["fit_raw"] >= 0.3 * maxfit and abs(STAGE_ORDER.index(y["stage"] or "create") - STAGE_ORDER.index(x["stage"] or "create")) <= 1:
                if l not in [c["id"] for c in comp]:
                    comp.append({"id": l, "name_ar": y["name_ar"], "name_en": y["name_en"], "because": f"linked to {x['id']}", "stage": y["stage"]})
    # tools
    meta_tool = META_TOOL_RX
    tools_hit = []
    short_fams = {f for x in short[:25] for f in x["families"]}
    try:
        r = subprocess.run([sys.executable, str(HERE / "hub.py"), "find", task + " " + " ".join(q[:20]), "--json"], capture_output=True, text=True, timeout=120)
        hf = json.loads(r.stdout)
        for t in hf.get("tools", [])[:20]:
            if meta_tool.match(t["id"]) and an["primary"] not in ("research", "unspecified"):
                continue
            reg_t = tools.get(t["id"], {})
            if not set(reg_t.get("families", [])) & short_fams:
                continue
            asked = norm_ar((task + " " + (terms or "")).lower())
            area_rx = AREA_NEEDS_WORDS.get(reg_t.get("area"))
            if area_rx and an["primary"] != reg_t.get("area") and not re.search(area_rx, asked):
                continue   # a specialised tool (3D, audio, drawing) only when the request is about that
            tool_rx = TOOL_NEEDS_WORDS.get(t["id"])
            if tool_rx and not re.search(tool_rx, asked):
                continue
            tools_hit.append({"id": t["id"], "title_ar": t.get("title_ar"), "title_en": t.get("title_en"), "area": t.get("area"),
                              "state": (t.get("readiness") or {}).get("state"), "missing": (t.get("readiness") or {}).get("missing", []),
                              "command": t.get("first_command") or ((reg_t.get("commands") or [{}])[0].get("example")),
                              "families": reg_t.get("families", [])})
        guides = [g.get("path") for g in hf.get("guides", [])[:6]]
    except Exception as exc:  # noqa: BLE001
        guides = [f"hub.py find failed: {exc}"]
    readiness = tool_readiness()
    libs = asset_libraries(task)
    # the user's own voice or footage goes through Montage Pro and real word timing in every plan
    forced = []
    if (an["constraints"]["own_assets"]["voice"] or an["constraints"]["own_assets"]["footage"]) and an["primary"] in ("video", "audio", "unspecified"):
        forced = [tid for tid in ("montage-pro", "repo-words-convert") if tid in tools]
    for tid in forced:
        if tid not in [t["id"] for t in tools_hit]:
            reg_t = tools[tid]
            tools_hit.insert(0, {"id": tid, "title_ar": reg_t.get("title_ar"), "title_en": reg_t.get("title_en"), "area": reg_t.get("area"),
                                 "state": readiness["state"].get(tid), "missing": [], "families": reg_t.get("families", []),
                                 "command": (reg_t.get("commands") or [{}])[0].get("example")})
    for lib in libs:
        for tid in dict.fromkeys(t for v in lib["plan_tools"].values() for t in v):
            if tid in tools and tid not in [t["id"] for t in tools_hit]:
                reg_t = tools[tid]
                tools_hit.insert(0 if tid == lib["id"] else len(tools_hit), {
                    "id": tid, "title_ar": reg_t.get("title_ar"), "title_en": reg_t.get("title_en"), "area": reg_t.get("area"),
                    "state": "ready (find)" if tid == lib["id"] else readiness["state"].get(tid), "missing": [], "families": reg_t.get("families", []),
                    "command": lib["command"] if tid == lib["id"] else ((reg_t.get("commands") or [{}])[0].get("example"))})
        for th in tools_hit:
            if th["id"] == lib["id"]:
                th.update(state="ready (find)", command=lib["command"])

    # plans = approaches
    arch = ARCHETYPES["publish"] if an.get("intent") == "publish" else ARCHETYPES.get(an["primary"], ARCHETYPES["_generic"])
    stages_tpl = arch["stages"]
    must_rows = [sp_by_id[i] for i in must_ids if i in sp_by_id]

    style_fams = {f for st_ in an["style"] for f in STYLE_FAMILIES.get(st_, [])}
    topic_fams = {f for t_ in an["topics"] for f in TOPIC_FAMILIES.get(t_, [])} if an["primary"] in ("research", "data", "document") else set()
    floor = MIN_FIT * maxfit

    def off_domain(x) -> bool:
        """Reverse-engineering tools are never a cross-domain integration for a job that inspects no binary or app, and a
        superpower built around a platform the request does not name never enters a plan."""
        if x["role"] == "must-have":
            return False
        if x.get("gated"):
            return True
        return x["group"] == "reverse" and an["primary"] != "reverse" and "reverse" not in an["topics"] and "reverse" not in an["deliverables"]

    def can_verify(x, fams) -> bool:
        """A verify-stage pick must be able to judge this deliverable, and a silent deliverable gets no sound checks."""
        f = set(x["families"])
        if an["silent"] and (f <= SOUND_FAMILIES or re.search(r"loudness|\blufs\b|\bsound\b|\baudio\b", x["name_en"].lower())):
            return False
        return bool(f & (vfam | fams))

    def plan(name, k, vsel, extra_cross, avoid=frozenset(), share_best=True, min_size=0):
        """One approach. Stage picks need the fit floor (must-haves are exempt). `avoid` keeps C a different method: B's
        own picks are not reused anywhere (stage picks, cross-domain extras, the top-up), except the best pick of a stage
        when share_best. `min_size` tops the plan up with further non-avoided stage candidates (never with B's picks)."""
        idea, fams = arch[name]
        fams = set(fams) | (style_fams if name != "A" else set()) | topic_fams
        boost = lambda x: x["score"] * (1.6 if fams and set(x["families"]) & fams else (0.6 if fams else 1.0))
        pool = [x for x in short if (x["role"] != "peripheral" or name == "C") and (x["role"] == "must-have" or x["fit_raw"] >= floor)
                and (x["role"] == "must-have" or (x["stage"] or "create") != "verify" or can_verify(x, fams)) and not off_domain(x)]
        chosen, stages = [], collections.OrderedDict((s, []) for s in stages_tpl)
        left = []
        for st in stages_tpl:
            cands = [x for x in pool if (x["stage"] or "create") == st and x["id"] not in [c["id"] for c in chosen]]
            cands.sort(key=lambda x: -boost(x))
            if avoid:
                head = cands[:1] if share_best else []
                cands = head + [x for x in cands[len(head):] if x["id"] not in avoid]
            picked = []
            for _ in range(min(k, len(cands))):   # a second pick in a stage prefers another family (an integration, not a twin)
                seen = {f for y in picked for f in y["families"]}
                rest = [x for x in cands if x not in picked]
                rest.sort(key=lambda x: -(boost(x) * (0.75 if set(x["families"]) & seen else 1.0)))
                picked.append(rest[0])
            for x in picked:
                chosen.append(x)
                stages[st].append(x)
            left += [x for x in cands if x not in picked]
        need_rows = must_rows if name != "A" else [sp_by_id[m["superpowers"][0]] for m in must_cov if m["superpowers"] and m["superpowers"][0] in sp_by_id]
        for x in need_rows:
            if x["id"] not in [c["id"] for c in chosen]:
                chosen.append(x)
                st = x["stage"] if x["stage"] in stages else stages_tpl[min(2, len(stages_tpl) - 1)]
                stages.setdefault(st, []).append(x)
        for v in vsel:
            if v["id"] not in [c["id"] for c in chosen]:
                chosen.append(v)
                stages.setdefault("verify", []).append(v)
        if extra_cross:
            for x in [y for y in short if y["role"] == "cross-domain" and y["id"] not in [c["id"] for c in chosen] and not off_domain(y)
                      and y["id"] not in avoid and ((y["stage"] or "create") != "verify" or can_verify(y, fams))][:extra_cross]:
                chosen.append(x)
                stages.setdefault(x["stage"] or "create", []).append(x)
        for x in sorted(left, key=lambda x: -boost(x)):   # top-up: deeper stage picks, never B's own
            if len(chosen) >= min_size:
                break
            if x["id"] not in [c["id"] for c in chosen] and x["id"] not in avoid:
                chosen.append(x)
                stages.setdefault(x["stage"] or "create", []).append(x)
        stages = collections.OrderedDict((s, stages[s]) for s in STAGE_ORDER if stages.get(s))
        return finish_plan(name, idea, chosen, stages)

    def finish_plan(name, idea, chosen, stages):
        atoms = sorted({h for x in chosen for h in x.get("hits", [])})
        badge_mix = collections.Counter(local_badge(by_id[a][0], pres) for a in atoms if a in by_id)
        req = sorted({k for x in chosen for k in x.get("requires", [])})
        missing = [k for k in req if pres.get(k) == "missing"]
        keys = [k for k in req if str(k).startswith("key:") and pres.get(k) != "present"]
        cf = {f for x in chosen for f in x.get("families", [])}
        tl = [t for t in tools_hit if set(t["families"]) & cf] or tools_hit[:2]
        lib_tools = forced + [tid for lib in libs for tid in lib["plan_tools"].get(name, [])]
        tl = [t for t in tools_hit if t["id"] in lib_tools] + [t for t in tl if t["id"] not in lib_tools]
        doc_share = sum(1 for x in chosen if x["local_badge"] in ("📄", "💡")) / max(1, len(chosen))
        uncovered = [m["need"] for m in must_cov if m["status"] == "covered" and not set(m["superpowers"]) & {x["id"] for x in chosen}]
        risks = []
        if missing:
            risks.append(f"{len(missing)} متطلبات ناقصة هنا: " + ", ".join(missing[:6]))
        if keys:
            risks.append("مفاتيح/خدمات: " + ", ".join(keys[:4]))
        if doc_share > 0.4:
            risks.append(f"{int(doc_share * 100)}% من القدرات الخارقة المختارة موصوفة فقط محليًا (📄) وتحتاج تنفيذًا")
        return {"name": name, "idea": idea, "definition": PLAN_DEFINITIONS[name],
                "meets_must_haves": not uncovered and all(m["status"] == "covered" for m in must_cov), "uncovered": uncovered,
                "superpowers": [{"id": x["id"], "name_ar": x["name_ar"], "name_en": x["name_en"], "stage": x["stage"], "group": x["group"],
                                 "score": x.get("score"), "local_badge": x["local_badge"], "role": x.get("role"),
                                 "contains": list(x.get("contains") or [])[:2]} for x in chosen],
                "stages": {s: [x["id"] for x in v] for s, v in stages.items()},
                "counts": {"groups": len({x["group"] for x in chosen}), "superpowers": len(chosen), "atoms_used": len(atoms),
                           "atoms_used_local_badges": dict(badge_mix), "members_in_scope": sum(x["size"] for x in chosen),
                           "tools": len(tl), "tools_ready": sum(1 for t in tl if str(t["state"]).startswith("ready"))},
                "groups": sorted({x["group"] for x in chosen}), "tools": tl[:6], "requires": req, "missing": missing, "keys": keys,
                "asset_routes": {lib["id"]: lib["routes"][name] for lib in libs if name in lib["routes"]},
                "risks": risks or ["لا مخاطر ظاهرة من البيانات"]}

    plans = {}
    if an["level"] != "L0":
        ids_of = lambda p_: {x["id"] for x in p_["superpowers"]}
        plans = {"A": plan("A", 1, verifiers[:1], 0, min_size=4), "B": plan("B", 2, verifiers[:2], 1)}
        b_ids = ids_of(plans["B"])
        fixed = must_ids | {v["id"] for v in verifiers}          # every plan must carry the must-haves; checks are listed apart
        b_core = frozenset(b_ids - fixed)
        c_ver = verifiers[:1] + verifiers[2:4] if len(verifiers) > 2 else verifiers[:2]   # another verification method
        avoid = frozenset(b_ids - must_ids - {v["id"] for v in c_ver})   # B's own picks, also a check C does not use

        def differs(p_):
            """C is another method, not B plus extras: it has picks of its own, keeps at most half of B's own picks and
            does not contain the whole of B."""
            c_ids = ids_of(p_)
            c_core = c_ids - fixed
            return bool(c_core - b_ids) and 2 * len(b_core & c_core) <= len(b_core) and not b_ids <= c_ids

        c_plan = plan("C", 3, c_ver, 3, avoid=avoid, min_size=len(b_ids))
        if not differs(c_plan):
            c_plan = plan("C", 3, c_ver, 3, avoid=avoid, share_best=False, min_size=len(b_ids))
        if not differs(c_plan):
            # the catalog offers no different method above the fit floor: C is honestly a depth level of B (never B twice)
            c_plan = plan("C", 3, verifiers[:4], 3, min_size=len(b_ids))
            if ids_of(c_plan) == b_ids:
                c_plan = finish_plan("C", arch["C"][0], [], {})
                c_plan.update(unavailable="لا يوجد في الكتالوج منهج مختلف ولا مستوى أعمق فوق حد الملاءمة؛ اعتمد B أو اقترح منهجك",
                              meets_must_haves=False, tools=[])
                c_plan["counts"].update(tools=0, tools_ready=0)
            else:
                c_plan["depth_of"] = "B"
                c_plan["idea"] += " — مستوى عمق لمنهج B نفسه (لا يوجد في الكتالوج منهج مختلف فوق حد الملاءمة)"
        plans["C"] = c_plan
    # recommendation with a reason
    if an["level"] == "L0":
        rec, why = None, "طلب L0: أجب مباشرة بلا خطط"
    elif an["ambition"] == "max" and not plans["C"].get("unavailable"):
        rec, why = "C", "طلبت أقصى جودة"
    elif an["primary"] in ("code", "reverse") and any(m["need"].startswith("اختبارات") for m in an["must_haves"]):
        rec, why = "B", "كود باختبارات: البناء النظيف بالاختبارات يحقق المتطلبات الإلزامية"
    elif an["ambition"] == "fast" or an["level"] == "L1":
        rec, why = "A", "طلب صغير أو طلبت السرعة"
    else:
        rec, why = "B", "أفضل توازن بين الجودة والتكلفة"
    if rec and plans and not plans[rec]["meets_must_haves"]:
        alt = next((k for k in "BC" if plans[k]["meets_must_haves"]), rec)
        if alt != rec:
            rec, why = alt, why + f"؛ الخطة الأصلية لا تغطي كل المتطلبات الإلزامية فاخترت {alt}"
    brief = {"schema": "kosif.skill-intelligence.v2", "protocol": PROTOCOL_VERSION, "protocol_doc": "PROTOCOL.md", "elapsed_s": None,
             "environment": environment(),
             "freshness": fresh, "coverage": receipt, "analysis": an, "query_terms": q[:50],
             "inventory": {"powers_total": receipt["records_on_disk"], "powers_relevant": len(relevant), "superpowers_total": len(sp.get("items", [])),
                           "superpowers_relevant": len(sp_rows), "shortlist": len(short), "groups_total": receipt["groups"], "families": receipt["families"],
                           "tools_total": readiness["summary"].get("tools"), "tools_ready": readiness["summary"].get("ready"),
                           "groups_ranked": [{"group": g, "score": round(v, 1)} for g, v in gsc.most_common()]},
             "must_have_coverage": must_cov, "excluded": excluded, "asset_libraries": libs,
             "top_powers": [{"id": r["id"], "name_ar": r["name_ar"], "name_en": r["name_en"], "group": r["group"], "catalog_status": r["status"],
                             "local_badge": local_badge(r, pres), "score": round(s, 2)} for s, r in relevant[:40]],
             "shortlist": short, "verifiers": [{"id": v["id"], "name_ar": v["name_ar"], "name_en": v["name_en"], "via": v["contains"][0],
                                                "via_family": v["via_family"]} for v in verifiers],
             "complements": comp[:8], "tools": tools_hit[:10], "guides": guides, "plans": plans, "recommended": rec, "recommended_reason": why,
             "approval_question": (f"أنصحك بالخطة {rec}. تحب أعرض لك تفاصيل القدرات وخطوات التنفيذ، ولا توافق على الخطة ونبدأ مباشرة؟" if rec else None),
             "plan_definitions": PLAN_DEFINITIONS,
             "reply_words": {"موافق": "نفّذ الخطة الموصى بها واقبل الإجابة المقترحة لكل سؤال مدرج",
                             "تفاصيل": "جدول أعمق للقدرات والتسلسل والاعتماديات والاختبارات",
                             "A/B/C": "اعتمد خطة أخرى", "D": "خطة مدمجة من عُقد تسمّيها من A/B/C",
                             "طوّر": "جولة نقد وتحسين وبحث عن تكاملات جديدة",
                             "نفّذ بأقصى قوة": "أعلى مستوى عملي دون التضحية بالاختبارات والترخيص", "نفّذ مباشرة": "تخطَّ العرض للمهام البسيطة",
                             "كمّل بدوني": "تابع بالإجابات المقترحة دون انتظاري"},
             "execution_words": {"كمّل": "تابع التنفيذ", "وقف": "أوقف التنفيذ", "تراجع": "تراجع عن آخر خطوة"}}
    brief["elapsed_s"] = round(time.time() - t0, 2)
    if not details:
        for x in brief["shortlist"]:
            x.pop("hits", None)
            x.pop("links", None)
    return brief


# ------------------------------------------------------------------ report
def render(b: dict) -> str:
    c, inv, an = b["coverage"], b["inventory"], b["analysis"]
    if an["level"] == "L0":
        return "\n".join([f"**المستوى L0 — مباشر.** الطلب قصير بلا ملفات أو إنتاج؛ الفحص الشامل غير لازم للإجابة "
                          f"(الإيصال متاح: {c['records_scanned']:,}/{c['records_on_disk']:,} {'✅' if c['complete'] else '❌'}).",
                          "أجب الآن بلغة المستخدم ولهجته، بلا خطط ولا سؤال موافقة."])
    L = [f"# تقرير بروتوكول ذكاء المهارات — KOSIF {b.get('protocol', PROTOCOL_VERSION)}", "", f"**المستوى {an['level']}** · **الطلب:** {an['request']}", "",
         "## بطاقة الطلب (مسودة آلية يكملها Claude)", "",
         f"- المخرج الأساسي: {an['primary']} ({', '.join(an['deliverables'])}) · الطموح: {an['ambition']}"
         + (f" · الأسلوب: {', '.join(an.get('style') or [])}" if an.get("style") else ""),
         f"- قيود: أرقام {an['constraints']['numbers'] or '—'} · مقاسات {an['constraints']['aspects'] or '—'} · ملفات موجودة {an['files_found'] or '—'}"
         + (" · **صوت المستخدم لا يُستبدل**" if an["constraints"]["own_assets"]["voice"] else "")
         + (" · **لقطات المستخدم لا تُستبدل**" if an["constraints"]["own_assets"]["footage"] else ""),
         "- أسئلة تغيّر النتيجة (مع الإجابة المقترحة؛ «موافق» تقبلها كلها): "
         + (" · ".join(f"{q_['question']} ← {q_['suggested_default']}" for q_ in an.get("questions") or []) or " · ".join(an["open_questions"]) or "—"), ""]
    if b["must_have_coverage"]:
        L += ["**جدول التغطية الإلزامي:**", "", "| المتطلب | القدرات الخارقة | قدرات ذرية | الحالة |", "|---|---|---|---|"]
        for m in b["must_have_coverage"]:
            L.append(f"| {m['need']} | {', '.join(f'{s} {bd}' for s, bd in zip(m['superpowers'], m['local_badges'])) or '—'} | {', '.join(m['atoms']) or '—'} | {'✅ مغطى' if m['status'] == 'covered' else '⚠️ فجوة: شغّل powers.py search'} |")
        L.append("")
    if b["excluded"]:
        L.append("**مستبعد بسبب القيود:** " + " · ".join(f"{e['id']} ({e['reason']})" for e in b["excluded"][:5]))
        L.append("")
    L += ["## نتيجة الجرد", "", "| البند | العدد |", "|---|---|",
          f"| السجلات المفحوصة / على القرص | {c['records_scanned']:,} / {c['records_on_disk']:,} {'✅' if c['complete'] else '❌'} |",
          f"| المجموعات / العائلات | {c['groups']} / {c['families']} |",
          f"| قدرات ذات صلة · قدرات خارقة ذات صلة · قائمة الترشيح | {inv['powers_relevant']:,} · {inv['superpowers_relevant']} · {inv['shortlist']} |",
          f"| تالف / غير مصنف | {c['broken_count']} / {c['unclassified_count']} |",
          f"| أدوات جاهزة الآن | {inv['tools_ready']} من {inv['tools_total']} |",
          f"| بصمة الكتالوج | `{c['catalog_sha256'][:16]}…` |", "",
          "الحداثة: " + " · ".join(f"{k} {'✅' if v.get('ok') else '❌ → ' + v.get('fix', '')}" for k, v in b["freshness"].items()), ""]
    for lib in b.get("asset_libraries", []):
        s = lib["stats"]
        lic = " · ".join(f"{k} {v:,}" for k, v in list(s["license"].items())[:4])
        L += [f"## مكتبات أصولك: {lib['title_ar']}", "",
              f"- {s['fonts']:,} خط فريد · {s['arabic']:,} يدعم العربية · {s['families']:,} عائلة · {s['ideas']} فئة أفكار · رخص: {lic}"
              + f" · معتمد لإعادة التوزيع: {s['redistribution_approved']}",
              f"- النمط المكتشف: {', '.join(lib['styles_detected']) or '—'}{' · ثنائي اللغة' if lib.get('bilingual') else ''} · ابحث: `{lib['command']}`",
              f"- مرشحات برخصة مفتوحة مُدّعاة (غير مؤكدة): {', '.join(lib.get('open_license_candidates') or []) or 'لا يوجد في مكتبتك لهذا النمط'}",
              f"- المكان: {lib['where']}", f"- البوابة: {lib['gate']}", ""]
    pl = b["plans"]
    L += ["## مقارنة الخطط (مناهج مختلفة؛ استبدلها بمناهجك من المرحلة 4 إن كانت أقوى)", "",
          "| البند | الخطة A | الخطة B | الخطة C |", "|---|---|---|---|"]
    row = lambda label, f: L.append(f"| {label} | " + " | ".join(f(pl[k]) for k in "ABC") + " |")
    row("المنهج", lambda p: p["idea"])
    row("تغطي كل الإلزامي؟", lambda p: "غير متاحة" if p.get("unavailable") else ("نعم" if p["meets_must_haves"] else "لا: " + ", ".join(p["uncovered"])[:60]))
    row("مجموعات · قدرات خارقة · قدرات مستخدمة · أدوات (جاهزة)", lambda p: f"{p['counts']['groups']} · {p['counts']['superpowers']} · {p['counts']['atoms_used']} · {p['counts']['tools']} ({p['counts']['tools_ready']})")
    row("شارات القدرات المستخدمة هنا", lambda p: " ".join(f"{k}{v}" for k, v in sorted(p["counts"]["atoms_used_local_badges"].items(), key=lambda kv: LOCAL_RANK.index(kv[0]))))
    row("متطلبات ناقصة", lambda p: str(len(p["missing"])))
    row("المخاطر", lambda p: " · ".join(p["risks"])[:150])
    if any(p.get("asset_routes") for p in pl.values()):
        row("مسار الخطوط", lambda p: " · ".join(p.get("asset_routes", {}).values())[:170] or "—")
    L += ["", "**المراحل:**"]
    for k in "ABC":
        L.append(f"- **{k}:** " + (pl[k]["unavailable"] if pl[k].get("unavailable") else
                                   " ← ".join(f"{s}: " + ", ".join(v) for s, v in pl[k]["stages"].items())
                                   + (f" (مستوى عمق لـ {pl[k]['depth_of']})" if pl[k].get("depth_of") else "")))
    L += ["", "## قائمة الترشيح (أعلى 12)", "", "| SP | القدرة الخارقة (تحتوي) | المجموعة | المرحلة | الدرجة | هنا | الدور |", "|---|---|---|---|---|---|---|"]
    for x in b["shortlist"][:12]:
        L.append(f"| {x['id']} | {x['name_ar']} ({'; '.join(x['contains'][:2])[:70]}) | {x['group']} | {x['stage']} | {x['score']} | {x['local_badge']} | {x['role']} |")
    if b["verifiers"]:
        L += ["", "**بوابات التحقق المقترحة:** " + " · ".join(f"{v['id']} {v['name_ar']}" for v in b["verifiers"])]
    if b["tools"]:
        L += ["", "**أدوات:** " + " · ".join(f"`{t['id']}` ({t['state']})" for t in b["tools"][:6])]
    if b["complements"]:
        L += ["", "**مكمّلات:** " + " · ".join(f"{c_['id']} {c_['name_ar']}" for c_ in b["complements"][:5])]
    L += ["", f"## التوصية الآلية: الخطة {b['recommended']} — {b['recommended_reason']}",
          "(Claude: التوصية النهائية منك بعد التشريح المسبق؛ اذكر السبب إن خالفت.)", "",
          "ردود بكلمة واحدة: " + " · ".join(f"`{k}`" for k in b["reply_words"]), "", f"**{b['approval_question']}**", ""]
    return "\n".join(L)


def summary(b: dict, out: Path) -> str:
    c = b["coverage"]
    lines = [f"brief → {out}", f"coverage {c['records_scanned']}/{c['records_on_disk']} complete={c['complete']} sha={c['catalog_sha256'][:12]}",
             f"level {b['analysis']['level']} · primary {b['analysis']['primary']} · recommended {b['recommended']} ({b['recommended_reason']})",
             "must-haves: " + ("; ".join(f"{m['need']}→{','.join(m['superpowers']) or 'GAP'}" for m in b["must_have_coverage"]) or "—"),
             "shortlist: " + " ".join(x["id"] for x in b["shortlist"][:10])]
    if b["plans"]:
        lines.append("plans: " + " · ".join(f"{k}={p['counts']['superpowers']}SP/{p['counts']['atoms_used']}atoms/{p['counts']['tools']}tools" for k, p in b["plans"].items()))
    lines.append(f"elapsed {b['elapsed_s']}s")
    return "\n".join(lines)


# ------------------------------------------------------------------ count / deep
def count(sp_ids, atom_ids=(), tool_ids=()) -> dict:
    scan = scan_catalog()
    by_id = {r["id"]: r for r in scan["records"]}
    reg, pres = requirement_presence()
    sp = {s["id"]: s for s in (jload(SP, {"items": []}) or {}).get("items", [])}
    tools = tool_registry()
    chosen = [sp[i] for i in sp_ids if i in sp]
    atoms = list(atom_ids) or [m["id"] for s in chosen for m in s["pipeline"]]
    fam2group = fam_to_group()
    badges = collections.Counter(local_badge(by_id[a], pres) for a in atoms if a in by_id)
    rd = tool_readiness()["state"]
    return {"superpowers": len(chosen), "unknown_superpowers": [i for i in sp_ids if i not in sp],
            "groups": len({fam2group.get(by_id[a]["family"]) for a in atoms if a in by_id}),
            "atoms_used": len(atoms), "atoms_used_local_badges": dict(badges), "members_in_scope": sum(s["size"] for s in chosen),
            "tools": len(tool_ids), "tools_ready": sum(1 for t in tool_ids if rd.get(t) == "ready"), "unknown_tools": [t for t in tool_ids if t not in tools]}


def deep(ids) -> str:
    out = []
    for i in ids:
        if re.match(r"^SP-\d+$", i):
            cmd = [sys.executable, str(HERE / "superpower_fusion.py"), "show", i]
        elif re.match(r"^[A-Z0-9]+-[A-Z]?\d+$", i):
            cmd = [sys.executable, str(HERE / "powers.py"), "show", i]
        else:
            cmd = [sys.executable, str(HERE / "hub.py"), "tool", i]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        out.append(f"===== {i}\n{(r.stdout or r.stderr).strip()}")
    return "\n\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("brief"); b.add_argument("task"); b.add_argument("--terms", default="", help="extra English keywords when routing misses")
    b.add_argument("--json", action="store_true"); b.add_argument("--out", type=Path); b.add_argument("--details", action="store_true")
    c = sub.add_parser("count"); c.add_argument("--sp", default=""); c.add_argument("--atoms", default=""); c.add_argument("--tools", default="")
    d = sub.add_parser("deep"); d.add_argument("ids", nargs="+")
    sub.add_parser("verify")
    a = ap.parse_args(argv)
    if a.cmd == "verify":
        scan = scan_catalog()
        fr = freshness(scan["records"])
        ok = scan["receipt"]["complete"] and all(v.get("ok") for v in fr.values())
        print(json.dumps({"pass": ok, "coverage": {k: v for k, v in scan["receipt"].items() if k != "group_sizes"}, "freshness": fr}, ensure_ascii=False, indent=1))
        return 0 if ok else 1
    if a.cmd == "count":
        split = lambda s: [x.strip() for x in s.split(",") if x.strip()]
        print(json.dumps(count(split(a.sp), split(a.atoms), split(a.tools)), ensure_ascii=False, indent=1))
        return 0
    if a.cmd == "deep":
        print(deep(a.ids))
        return 0
    br = build_brief(a.task, a.details, a.terms)
    if a.out:
        a.out.parent.mkdir(parents=True, exist_ok=True)   # the work dir may not exist yet
        a.out.write_text(json.dumps(br, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(summary(br, a.out))
    elif a.json:
        print(json.dumps(br, ensure_ascii=False, indent=1))
    else:
        print(render(br))
    return 0 if br["coverage"]["complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
