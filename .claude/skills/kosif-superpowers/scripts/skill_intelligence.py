#!/usr/bin/env python3
"""KOSIF Universal Skill Intelligence Protocol — محرك بروتوكول ذكاء المهارات الشامل (USIP v2.1).

The machine half of PROTOCOL.md. For any request it:
  0. checks the environment and that every derived index is fresh,
  1. drafts a request card: protocol level (L0–L3), deliverable, constraints, own-asset rules, must-haves,
  2. scans 100% of the catalog records (every data/powers/*.json row) and returns a SHA-256 coverage receipt
     that fails closed when any record is unreadable, unclassified or duplicated,
  3. ranks groups, fused superpowers, powers and runnable tools; a must-have layer forces in what the request
     cannot do without, a constraint layer excludes what would replace the user's own assets, fit gates keep
     unrelated "creative" picks out,
  4. scores candidates (fit 35 · integration 20 · feasibility 15 · evidence 10 · cost 10 · creativity 10) with
     LOCAL badges (proof in this checkout, requirements present here),
  5. drafts plans A/B/C as different APPROACHES for the deliverable type, each covering every must-have and
     ending in a verifier, with defined counts, risks, a recommendation and its reason, and the approval question.

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
WEIGHTS = {"fit": 35, "integration": 20, "feasibility": 15, "evidence": 10, "cost": 10, "creativity": 10}
LOCAL_RANK = ["✅", "🟢", "📦", "🔑", "📄", "💡"]
LOCAL_EVIDENCE = {"✅": 1.0, "🟢": 0.8, "📦": 0.55, "🔑": 0.4, "📄": 0.25, "💡": 0.1}
STAGE_ORDER = ["understand", "plan", "create", "refine", "assemble", "verify", "deliver"]


# ------------------------------------------------------------------ text
def norm_ar(s: str) -> str:
    s = re.sub(r"[ً-ْـ]", "", s or "")
    return s.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا").replace("ة", "ه").replace("ى", "ي")


_STOP_RAW = ("the and for with from that this your make build want need what how please a an is are of to my can i you me it in on "
             "عايز اعمل عمل من في على عن الى إلى و ال دي ده دول هذا هذه لي هل ممكن اريد أريد ابغى ابي عاوز يا مع كل بعد قبل "
             "فيه يكون ابني صغير بسيط بسيطة عندي عشان علشان بتاع بتاعي اللي الذي التي انا أنا لو او أو ثم كده كدا ازاي إزاي")
STOP = {norm_ar(w) for w in _STOP_RAW.split()}
ALIASES = {  # protocol-specific Arabic/Egyptian → English bridges (checked against catalog wording)
    "محاسبه": "accounting bookkeeping ledger", "محاسبة": "accounting bookkeeping ledger", "مخزون": "inventory stock",
    "مبيعات": "sales", "تقرير": "report", "شهري": "monthly", "فاتوره": "invoice", "فواتير": "invoice",
    "ترجم": "translate translation", "ترجمه": "translation subtitles captions", "فويس": "voice narration audio", "صوتي": "voice narration audio",
    "بصوتي": "voice narration audio", "تطبيق": "app application", "ويب": "web", "اختبارات": "tests testing", "اختبار": "test testing",
    "شخصيه": "character", "كرتونيه": "cartoon character", "كرتوني": "cartoon character", "ريلز": "reels vertical short",
    "موشن": "motion graphics animation", "جرافيك": "graphics", "متحركه": "animated kinetic", "كلمات": "words captions kinetic typography",
    "عربيه": "arabic", "عربي": "arabic", "ميزه": "feature", "ميزة": "feature", "مشابهه": "similar original", "مشابهة": "similar original",
    "حلل": "analyze analysis", "هندسه": "engineering", "عكسيه": "reverse", "مثبت": "installed", "مسار": "path",
    "مونتاج": "montage edit cut", "فيديو": "video", "صوره": "image photo", "صور": "images photos", "رسم": "draw drawing",
    "ارسم": "draw", "خط": "font typography", "خطوط": "fonts typography", "فونت": "font typeface", "كوفي": "kufi arabic font",
    "ديواني": "diwani calligraphy", "بوستر": "poster", "لوجو": "logo brand", "شعار": "logo brand", "بيانات": "data", "مستند": "document", "بحث": "search research",
}


def tokens(s: str) -> list:
    s = norm_ar(str(s or "").lower())
    s = re.sub(r"[،؛؟٪-٭۔«»“”\"'(),.:;!?،]", " ", s)
    return [w for w in re.findall(r"[a-z0-9][a-z0-9+#-]*[a-z0-9+#]|[a-z0-9]|[ء-يٱ-ۓ]{2,}", s) if w not in STOP]


def expand(query: str, df: collections.Counter, extra: str = "") -> list:
    """Query words + aliases + clitic stems that exist in the catalog vocabulary (and only then)."""
    words = tokens(query) + tokens(extra)
    out = list(words)
    for w in words:
        if w in ALIASES:
            out += tokens(ALIASES[w])
        if re.match(r"[؀-ۿ]", w) and df.get(w, 0) == 0:
            for pre in ("وال", "بال", "لل", "ال", "و", "ب", "ل", "ف"):
                if w.startswith(pre) and len(w) - len(pre) >= 3:
                    stem = w[len(pre):]
                    if df.get(stem, 0) > 0:
                        out.append(stem)
                        if stem in ALIASES:
                            out += tokens(ALIASES[stem])
                    break
    return list(dict.fromkeys(x for x in out if x and x not in STOP))


def jload(p: Path, default=None):
    try:
        return json.loads(p.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        return default


# ------------------------------------------------------------------ stage 0
def environment() -> dict:
    env = {"python": sys.version.split()[0], "tools": {b: bool(shutil.which(b)) for b in ("ffmpeg", "ffprobe", "node", "git", "rea", "blender", "yt-dlp")}}
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
    ("reverse", r"هندسه عكسيه|جفرا|ghidra|\brea\b|reverse|binary|\.exe|\.dll|\.apk|app\.asar|\basar\b|electron|الكترون"),
    ("code", r"كود|برمجه|تطبيق|موقع|سكربت|\bbug\b|\bcode\b|\bapp\b|website|script|\bapi\b|repo|مستودع|برنامج"),
    ("video", r"فيديو|مونتاج|ريلز|موشن|انيميشن|تحريك|فيلم|video|montage|\breels?\b|motion|animation|film|\bmp4\b"),
    ("audio", r"بودكاست|موسيقى|اغنيه|podcast|music|song"),
    ("3d", r"ثلاثي|\b3d\b|بلندر|blender|\bglb\b|three\.?js"),
    ("image", r"صوره|صور|تصميم|بوستر|شعار|لوجو|image|photo|poster|logo|design|\bpng\b|\bjpg\b"),
    ("data", r"بيانات|اكسل|جدول|\bdata\b|\bcsv\b|excel|chart|dashboard"),
    ("document", r"تقرير|مستند|وورد|\bpdf\b|عرض تقديمي|شرائح|report|document|docx|slides|deck|مقال|article"),
    ("research", r"ابحث|مصادر|research|sources|قارن|compare"),
]
SHORT_INTENTS = r"^(ترجم|translate|اشرح|explain|عرف|define|ما معني|ايه معني|صحح|proofread|rename|اعد صياغه|لخص|summari[sz]e)"
FAST_RX = r"(بسرعه|نسخه (بسيطه|سريعه)|مختصر|quick version|\bquick\b|\bfast\b|سطر واحد|one line)"
MAX_RX = r"(باقصي|اقصي قوه|كل القدرات|\bmaximum\b|\bmax\b|ultimate|best possible|سينمائي|cinematic)"
OWN_VOICE_RX = r"(بصوتي|صوتي|فويس|تسجيلي|my (own )?voice|my recording|i recorded)"
OWN_FOOTAGE_RX = r"(فيديو(هات)? (بتاعي|الخاص بي)|لقطاتي|صوري|my footage|my (own )?video|my photos)"
PLATFORM_RX = {"os:macos": r"mac|ماك|\bios\b|xcode|apple", "engine:android": r"android|apk|اندرويد", "os:windows": r"windows|ويندوز|\.exe"}
MUST_HAVE = [
    ("توقيت الكلمات من صوت المستخدم", r"(كلمات|نص|ترجمه|captions?|subtitles?|words).{0,40}(صوت|فويس|voice|audio)|(صوت|فويس|voice).{0,40}(كلمات|ترجمه|captions?|words)",
     "transcription word timestamps whisper alignment words.json word timing sync"),
    ("نص عربي صحيح RTL", r"عربي|عربيه|arabic", "arabic rtl shaping whole word kinetic typography"),
    ("اختبارات آلية", r"اختبار|tests?\b|testing", "unit tests test suite regression"),
    ("تقرير PDF", r"\bpdf\b", "pdf report generate"),
    ("شخصية متحركة", r"شخصيه|character", "character rig animation blink walk wave"),
    ("مقاس ريلز ومناطق آمنة", r"ريلز|reels?|9:16|تيك ?توك|tiktok|shorts", "vertical 9:16 reels safe area"),
    ("تحليل تطبيق Electron بأدلة", r"electron|asar|الكترون", "electron asar javascript application analysis"),
    ("بناء أصلي نظيف (clean-room) مع بوابة أصالة", r"(ابني|ابن|build|اعمل).{0,40}(مشابه|similar|زي|like)|ميزه مشابهه", "originality check clean room reimplementation specification"),
    ("محاسبة ومخزون بأرقام صحيحة", r"محاسب|مخزون|inventory|accounting|ledger", "accounting ledger inventory bookkeeping"),
    ("مونتاج وقطع", r"مونتاج|montage", "montage edit cut transitions"),
    ("ترجمة", r"^ترجم|translate", "translation"),
    ("خط مناسب برخصة مؤكدة", None, "arabic font typography font matching fonts license kinetic typography lettering"),
]
_AR = "\u0621-\u064a"
FONT_RX = (rf"(?<![{_AR}])[وف]?(?:بال|لل|ال|ب|ل)?(?:خطوط|خط|فونتات|فونت)(?![{_AR}])|كوفي|ديواني|كاليجراف|تايبو|حروفيه|"
           r"\bfonts?\b|typeface|typograph|lettering|calligraph|\bglyphs?\b|شعار|لوجو|\blogos?\b|بوستر|\bposters?\b")
MUST_HAVE = [(n, FONT_RX if rx is None else rx, terms) for n, rx, terms in MUST_HAVE]
ARABIC_TERMS = {  # the Arabic-text need means different checks per deliverable
    "image": "arabic shaping harfbuzz glyph ligature font logo poster rtl lettering",
    "document": "arabic rtl docx pdf shaping fonts document",
    "video": "arabic rtl shaping whole word kinetic typography captions",
    "code": "arabic rtl bidi ui localization shaping",
    "3d": "arabic shaping 3d text extrude glyph",
}
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
        idx = files[-1]
        d = jload(idx, {}) or {}
        fonts = d.get("fonts", [])
        lic = collections.Counter(f.get("license_status", "?") for f in fonts)
        styles = []
        for w in re.findall(r"[\w]+", low):
            s = FONT_STYLES.get(w) or FONT_STYLES.get(w[2:] if w.startswith("ال") else w)
            if s and s not in styles:
                styles.append(s)
        arabic = bool(re.search(r"عربي|arabic|[\u0621-\u064a]", low))
        q = " ".join(styles) or ("arabic" if arabic else "display")
        rel = idx.relative_to(SKILL).as_posix()
        out.append({"id": lib["id"], "title_ar": lib["title_ar"], "title_en": lib["title_en"], "index": rel,
                    "stats": {"fonts": len(fonts), "arabic": sum(1 for f in fonts if f.get("has_arabic")),
                              "families": (d.get("script_coverage") or {}).get("unique_font_families", 0),
                              "ideas": len(d.get("typography_design_ideas", [])), "license": dict(lic.most_common()),
                              "redistribution_approved": sum(1 for f in fonts if f.get("redistribution_approved"))},
                    "styles_detected": styles,
                    "command": f'python3 scripts/telegram_typography_atlas.py find --index {rel} "{q}"' + (" --arabic-only" if arabic else "") + " --limit 20",
                    "where": lib["where"], "gate": lib["gate"], "routes": lib["routes"], "plan_tools": lib["plan_tools"]})
    return out
VERIFY_TERMS = {
    "video": "verify video delivery gate ffprobe loudness frames qa", "audio": "loudness lufs verify audio qa",
    "code": "tests test suite regression golden unit coverage", "reverse": "evidence originality tests golden parity",
    "image": "contrast check visual qa", "3d": "frames verify render check", "data": "validation check numbers reconcile",
    "document": "proofread review check anchor numbers", "research": "citation fact check sources", "text": "proofread review language",
}
ARCHETYPES = {
    "video": {"stages": STAGE_ORDER,
              "A": ("محرك المونتاج والقوالب الجاهزة (ffmpeg/Montage Pro)", ["transitions-cuts", "photo-video-footage", "formats-platforms", "video-download", "music-beat-sound", "audio-sync-captions", "runnable-tools"]),
              "B": ("محرك موشن مخصص متزامن مع الكلمات (SVG/HTML)", ["hand-drawn-draw-on", "typography-arabic", "typography-latin", "easing-timing-rhythm", "characters-rigs", "audio-sync-captions", "shapes-morph-geometry", "camera-composition-layout", "runnable-tools"]),
              "C": ("خط سينمائي متعدد المحركات (3D/Remotion/مؤثرات)", ["3d-spatial", "engines-render-pipeline", "light-glow-bloom", "particles-fluids-physics", "color-palette-grading", "texture-material", "characters-rigs", "typography-arabic", "audio-sync-captions"])},
    "code": {"stages": ["understand", "plan", "create", "verify", "deliver"],
             "A": ("إعادة استخدام مكتبة/قالب جاهز وتهيئته", ["atlas-code", "apps-artifacts", "atlas-build", "code-engineering"]),
             "B": ("بناء نظيف بمعمارية واختبارات", ["code-engineering", "api-testing", "verification-evals", "security-safety", "atlas-code", "documents-office"]),
             "C": ("بناء + معايير أداء وتكافؤ وأمان وCI", ["code-engineering", "api-testing", "verification-evals", "security-safety", "qa-verification", "atlas-mind", "planning-execution", "atlas-code"])},
    "reverse": {"stages": ["understand", "plan", "create", "verify", "deliver"],
                "A": ("فحص ثابت بـ REA ثم تقرير بنية", ["software-investigation", "runnable-tools"]),
                "B": ("فحص ثابت + بناء أصلي نظيف ببوابة أصالة", ["software-investigation", "code-engineering", "verification-evals", "runnable-tools"]),
                "C": ("فحص ثابت وديناميكي + اختبارات تكافؤ سلوكي", ["software-investigation", "code-engineering", "verification-evals", "qa-verification", "app-feature-transfer", "runnable-tools"])},
    "image": {"stages": ["understand", "plan", "create", "refine", "verify", "deliver"],
              "A": ("خط برخصة مؤكدة + تكوين بسيط واضح", ["typography-arabic", "typography-latin", "brand-logo-identity", "camera-composition-layout", "runnable-tools"]),
              "B": ("تصميم مخصص: مطابقة خطوط + تكوين متجهي + فحص قراءة وتباين", ["typography-arabic", "typography-latin", "brand-logo-identity", "shapes-morph-geometry", "color-palette-grading", "qa-verification", "runnable-tools"]),
              "C": ("حروف أصلية من الصفر + هوية كاملة + موك أب وحركة", ["typography-arabic", "brand-logo-identity", "hand-drawn-draw-on", "shapes-morph-geometry", "texture-material", "light-glow-bloom", "creativity-engine", "easing-timing-rhythm"])},
    "_generic": {"stages": STAGE_ORDER,
                 "A": ("المسار الأقصر بأقوى القدرات الجاهزة", []), "B": ("مسار متوازن مع تكامل من مجالات أخرى", []), "C": ("مسار شامل بمراحل ونقاط توقف", [])},
}


# domain affinity per primary deliverable: off-domain clusters are down-weighted, never hidden from the receipt
AFFINITY = {"code": {"motion": 0.4, "reverse": 0.4}, "reverse": {"motion": 0.4}, "data": {"motion": 0.5, "reverse": 0.4},
            "document": {"motion": 0.5, "reverse": 0.4}, "research": {"motion": 0.5, "reverse": 0.4}, "text": {"motion": 0.5, "reverse": 0.3},
            "video": {"reverse": 0.3}, "audio": {"reverse": 0.3}, "image": {"reverse": 0.3, "docs": 0.5, "code": 0.6}, "3d": {"reverse": 0.3}}


def affinity(primary: str, sp_domain: str, families) -> float:
    a = AFFINITY.get(primary, {})
    f = a.get("reverse", 1.0) if "software-investigation" in families else 1.0
    return min(f, a.get(sp_domain, 1.0))


def analyse(task: str) -> dict:
    low = norm_ar(task.lower())
    deliver = [k for k, rx in DELIVERABLES if re.search(rx, low)]
    numbers = re.findall(r"\d+(?:[.,]\d+)?\s*(?:ثانيه|ثواني|ث|دقيقه|دقائق|sec|min|fps|%|k)?", task)
    aspects = re.findall(r"\b(?:9:16|16:9|1:1|4:5|21:9|4:3)\b", task)
    paths = re.findall(r"[\w./\\:-]+\.(?:mp4|mov|wav|mp3|m4a|png|jpg|jpeg|pdf|docx|xlsx|csv|json|py|js|ts|blend|glb|exe|dll|apk|asar)\b", task, re.I)
    existing = [p for p in paths if Path(p).expanduser().exists()]
    ntok = len(tokens(task))
    ambition = "max" if re.search(MAX_RX, low) else ("fast" if re.search(FAST_RX, low) else "balanced")
    if re.search(SHORT_INTENTS, low.strip()) and not paths and ntok <= 14 and not set(deliver) & {"video", "code", "reverse", "3d"}:
        level = "L0"
    elif ambition == "max":
        level = "L3"
    elif not paths and ntok <= 8 and not set(deliver) & {"video", "code", "reverse", "3d", "data"}:
        level = "L1"
    else:
        level = "L2"
    primary = deliver[0] if deliver else ("text" if level == "L0" else "unspecified")
    own = {"voice": bool(re.search(OWN_VOICE_RX, low)), "footage": bool(re.search(OWN_FOOTAGE_RX, low))}
    musts = [{"need": n, "terms": ARABIC_TERMS.get(primary, terms) if n.startswith("نص عربي") else terms} for n, rx, terms in MUST_HAVE if re.search(rx, low)]
    platforms = [k for k, rx in PLATFORM_RX.items() if re.search(rx, low)]
    questions = []
    if primary == "video" and not aspects:
        questions.append("المقاس والمنصة (9:16 ريلز؟ 16:9 يوتيوب؟)")
    if (own["voice"] or own["footage"] or primary in ("reverse",)) and not existing:
        questions.append("أين الملف المصدر؟ (رفع في الجلسة، مسار على جهازك عبر Remote Desktop Commander بإذنك، أو رابط)")
    return {"request": task, "level": level, "deliverables": deliver or [primary], "primary": primary, "ambition": ambition,
            "constraints": {"numbers": [n.strip() for n in numbers if n.strip()], "aspects": aspects, "own_assets": own, "platforms_mentioned": platforms},
            "files_mentioned": paths, "files_found": existing, "must_haves": musts, "open_questions": questions,
            "claude_must_answer": ["ماذا يريد حرفيًا؟", "ما النتيجة النهائية؟", "ما المشكلة الأساسية؟", "المتطلبات الصريحة والضمنية",
                                   "مستوى الجودة والجمهور", "القيود: وقت/تكلفة/أجهزة/صلاحيات/ترخيص", "معايير نجاح قابلة للقياس", "طريقة أذكى من وصف المستخدم؟"]}


# ------------------------------------------------------------------ ranking
def build_df(records):
    df = collections.Counter()
    toks = []
    for r in records:
        t = collections.Counter(tokens(r["text"]))
        toks.append(t)
        for w in t:
            df[w] += 1
    return df, toks


def score_records(records, toks, df, words):
    n = len(records)
    out = []
    for r, t in zip(records, toks):
        name = set(tokens(r["name_en"] + " " + r["name_ar"]))
        s = 0.0
        for w in words:
            tf = t.get(w, 0)
            if not tf and len(w) >= 4:
                tf = sum(c for k, c in t.items() if k.startswith(w))
            if tf:
                s += (1 + math.log(1 + tf)) * math.log(1 + n / (1 + df.get(w, 0))) * (2.2 if w in name else 1.0)
        out.append(s)
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


def build_brief(task: str, details=False, terms: str = "") -> dict:
    t0 = time.time()
    scan = scan_catalog()
    records, receipt = scan["records"], scan["receipt"]
    fresh = freshness(records)
    an = analyse(task)
    df, toks = build_df(records)
    q = expand(task, df, terms)
    scores = score_records(records, toks, df, q)
    by_id = {r["id"]: (r, s) for r, s in zip(records, scores)}
    reg, pres = requirement_presence()
    tools = tool_registry()
    pid2tool = {t.get("power_id"): t for t in tools.values() if t.get("power_id")}
    fam2group = fam_to_group()

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
    excluded = []
    sp_rows = []
    for s in sp.get("items", []):
        ms = [(by_id[m["id"]][0], by_id[m["id"]][1]) for m in s["pipeline"] if m["id"] in by_id]
        rel = sorted((sc for _r, sc in ms), reverse=True)
        fit = sum(rel[:5]) + 0.25 * sum(rel[5:])
        if fit <= 0:
            continue
        fam_count = collections.Counter(a["family"] for a, _ in ms)
        if own_voice and (fam_count.get("voice-tts", 0) >= 0.5 * len(ms) or re.search(r"\btts\b|text.to.speech|voice clon|elevenlabs|voice costume", s["name_en"].lower())):
            excluded.append({"id": s["id"], "name": s["name_en"], "reason": "يستبدل صوت المستخدم (TTS/استنساخ) والطلب على صوته هو"})
            continue
        plat = {k for a, _ in ms for k in a.get("requires") or [] if k in PLATFORM_RX}
        if plat and not plat & mentioned_platforms:
            fit *= 0.3
        dom = collections.Counter(a.get("domain") or "motion" for a, _ in ms).most_common(1)[0][0]
        fit *= affinity(an["primary"], dom, fam_count)
        hits = sorted(((a, sc) for a, sc in ms if sc > 0), key=lambda x: -x[1])
        badges = [local_badge(a, pres) for a, _ in (hits or ms)]
        lb = min(badges, key=LOCAL_RANK.index) if badges else "📄"
        ready_local = sum(1 for a, _ in ms if local_badge(a, pres) in ("✅", "🟢"))
        sp_rows.append({"id": s["id"], "name_ar": s["name_ar"], "name_en": s["name_en"], "group": plan_group(s.get("families", {}), s["pipeline"]), "domain": dom,
                        "families": list(fam_count), "stage": stage_of.get(s["id"], "create"), "size": s["size"], "catalog_best": s["best"],
                        "local_badge": lb, "ready_local": ready_local, "requires": s.get("requires", []), "links": [l["id"] for l in s.get("links", [])],
                        "fit_raw": fit, "hits": [a["id"] for a, _ in hits], "contains": [a["name_en"] for a, _ in hits[:3]],
                        "badge_mix_local": dict(collections.Counter(badges))})
    sp_rows.sort(key=lambda x: -x["fit_raw"])
    maxfit = max([x["fit_raw"] for x in sp_rows] or [1.0])
    gsc = collections.Counter()
    for x in sp_rows[:80]:
        gsc[x["group"]] += x["fit_raw"]
    top_groups = [g for g, _ in gsc.most_common(2)]

    # must-have layer: each need gets its own sub-ranking and at least one superpower
    must_cov = []
    must_ids = set()
    top_atom = max([s for s, _ in relevant[:1]] or [1.0])
    sp_by_id = {x["id"]: x for x in sp_rows}
    atom2sp = {m["id"]: s["id"] for s in sp.get("items", []) for m in s["pipeline"]}
    for need in an["must_haves"]:
        w = expand(need["terms"], df)
        sub = score_records(records, toks, df, w)
        best_atoms = sorted(((sc, r) for r, sc in zip(records, sub) if sc > 0), key=lambda x: -x[0])[:16]
        agg = collections.Counter()
        for sc, r in best_atoms:
            sid = atom2sp.get(r["id"])
            if sid and sid in sp_by_id:
                ctx = by_id[r["id"]][1] / top_atom   # how much this atom also matches the whole request
                agg[sid] += sc * (1 + ctx) * affinity(an["primary"], sp_by_id[sid]["domain"], sp_by_id[sid]["families"])
        ranked_need = agg.most_common(2)
        pick = [ranked_need[0][0]] if ranked_need else []
        if len(ranked_need) > 1 and ranked_need[1][1] >= 0.75 * ranked_need[0][1]:
            pick.append(ranked_need[1][0])
        must_ids.update(pick)
        must_cov.append({"need": need["need"], "superpowers": pick, "atoms": [r["id"] for _, r in best_atoms[:4]],
                         "status": "covered" if pick else "gap", "local_badges": [sp_by_id[p]["local_badge"] for p in pick]})
    # scoring
    short = sp_rows[:60] + [sp_by_id[i] for i in must_ids if i not in {x["id"] for x in sp_rows[:60]}]
    short_ids = {x["id"] for x in short}
    for x in short:
        integ = len([l for l in x["links"] if l in short_ids])
        miss = [k for k in x["requires"] if pres.get(k) == "missing"]
        keys = [k for k in x["requires"] if str(k).startswith("key:") and pres.get(k) != "present"]
        strong_outside = x["group"] not in top_groups and x["fit_raw"] >= 0.4 * maxfit
        sc = {"fit": x["fit_raw"] / maxfit, "integration": min(1.0, integ / 3), "feasibility": x["ready_local"] / max(1, x["size"]),
              "evidence": LOCAL_EVIDENCE.get(x["local_badge"], 0.2), "cost": 1.0 - min(1.0, 0.25 * len(miss) + 0.5 * len(keys)),
              "creativity": 1.0 if strong_outside else 0.3 * x["fit_raw"] / maxfit}
        x["score"] = round(sum(WEIGHTS[k] * v for k, v in sc.items()), 1)
        x["score_parts"] = {k: round(WEIGHTS[k] * v, 1) for k, v in sc.items()}
        x["missing"], x["needs_key"] = miss, keys
        x["role"] = "must-have" if x["id"] in must_ids else ("core" if x["group"] in top_groups else ("cross-domain" if strong_outside else "peripheral"))
    short.sort(key=lambda x: (x["role"] != "must-have", -x["score"]))
    # verifiers by deliverable
    vt = expand(VERIFY_TERMS.get(an["primary"], VERIFY_TERMS["text"]), df)
    vsc = score_records(records, toks, df, vt)
    vagg = collections.Counter()
    for r, sc in zip(records, vsc):
        if sc > 0 and atom2sp.get(r["id"]):
            sid = atom2sp[r["id"]]
            base = sp_by_id.get(sid)
            aff = affinity(an["primary"], base["domain"], base["families"]) if base else affinity(an["primary"], r.get("domain") or "motion", [r.get("family")])
            vagg[sid] += sc * aff
    verifiers = []
    for sid, _ in vagg.most_common(40):
        s = sp_by_id.get(sid) or next(({"id": y["id"], "name_ar": y["name_ar"], "name_en": y["name_en"], "group": "quality", "stage": "verify",
                                         "size": y["size"], "catalog_best": y["best"], "local_badge": "📄", "ready_local": 0, "requires": y.get("requires", []),
                                         "links": [], "fit_raw": 0, "hits": [], "contains": [], "families": list(y.get("families", {})), "score": 0,
                                         "role": "verifier", "missing": [], "needs_key": []} for y in sp.get("items", []) if y["id"] == sid), None)
        if not s or s.get("needs_key"):
            continue
        if any(str(k).startswith("key:") for k in s.get("requires", [])):
            continue
        s = dict(s)
        s["stage"], s["role"] = "verify", "verifier"
        verifiers.append(s)
        if len(verifiers) >= 3:
            break
    # complements: linked to a top pick, relevant themselves, same or adjacent stage
    comp = []
    for x in short[:8]:
        for l in x["links"]:
            y = sp_by_id.get(l)
            if y and l not in short_ids and y["fit_raw"] >= 0.3 * maxfit and abs(STAGE_ORDER.index(y["stage"] or "create") - STAGE_ORDER.index(x["stage"] or "create")) <= 1:
                if l not in [c["id"] for c in comp]:
                    comp.append({"id": l, "name_ar": y["name_ar"], "name_en": y["name_en"], "because": f"linked to {x['id']}", "stage": y["stage"]})
    # tools
    meta_tool = re.compile(r"^(capability-|atlas-|ai-tool-discovery|boot|hub$|powers|skill-intelligence|superpower-fusion|kosif-groups|capability|requirements|probe-env|catalog-|check-skill|relabel|build-chapters|package-skill|rea-creative)")
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
            tools_hit.append({"id": t["id"], "title_ar": t.get("title_ar"), "title_en": t.get("title_en"), "area": t.get("area"),
                              "state": (t.get("readiness") or {}).get("state"), "missing": (t.get("readiness") or {}).get("missing", []),
                              "command": t.get("first_command") or ((reg_t.get("commands") or [{}])[0].get("example")),
                              "families": reg_t.get("families", [])})
        guides = [g.get("path") for g in hf.get("guides", [])[:6]]
    except Exception as exc:  # noqa: BLE001
        guides = [f"hub.py find failed: {exc}"]
    readiness = tool_readiness()
    libs = asset_libraries(task)
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
    arch = ARCHETYPES.get(an["primary"], ARCHETYPES["_generic"])
    stages_tpl = arch["stages"]
    must_rows = [sp_by_id[i] for i in must_ids if i in sp_by_id]

    def plan(name, k, n_verify, extra_cross):
        idea, fams = arch[name]
        fams = set(fams)
        pool = [x for x in short if x["role"] != "peripheral" or name == "C"]
        chosen, stages = [], collections.OrderedDict((s, []) for s in stages_tpl)
        for st in stages_tpl:
            cands = [x for x in pool if (x["stage"] or "create") == st and x["id"] not in [c["id"] for c in chosen]]
            cands.sort(key=lambda x: -(x["score"] * (1.6 if fams and set(x["families"]) & fams else (0.6 if fams else 1.0))))
            for x in cands[:k]:
                chosen.append(x)
                stages[st].append(x)
        need_rows = must_rows if name != "A" else [sp_by_id[m["superpowers"][0]] for m in must_cov if m["superpowers"] and m["superpowers"][0] in sp_by_id]
        for x in need_rows:
            if x["id"] not in [c["id"] for c in chosen]:
                chosen.append(x)
                st = x["stage"] if x["stage"] in stages else stages_tpl[min(2, len(stages_tpl) - 1)]
                stages.setdefault(st, []).append(x)
        for v in verifiers[:n_verify]:
            if v["id"] not in [c["id"] for c in chosen]:
                chosen.append(v)
                stages.setdefault("verify", []).append(v)
        if extra_cross:
            for x in [y for y in short if y["role"] == "cross-domain" and y["id"] not in [c["id"] for c in chosen]][:extra_cross]:
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
        lib_tools = [tid for lib in libs for tid in lib["plan_tools"].get(name, [])]
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
        return {"name": name, "idea": idea, "meets_must_haves": not uncovered and all(m["status"] == "covered" for m in must_cov), "uncovered": uncovered,
                "superpowers": [{"id": x["id"], "name_ar": x["name_ar"], "name_en": x["name_en"], "stage": x["stage"], "group": x["group"],
                                 "score": x.get("score"), "local_badge": x["local_badge"], "role": x.get("role")} for x in chosen],
                "stages": {s: [x["id"] for x in v] for s, v in stages.items()},
                "counts": {"groups": len({x["group"] for x in chosen}), "superpowers": len(chosen), "atoms_used": len(atoms),
                           "atoms_used_local_badges": dict(badge_mix), "members_in_scope": sum(x["size"] for x in chosen),
                           "tools": len(tl), "tools_ready": sum(1 for t in tl if str(t["state"]).startswith("ready"))},
                "groups": sorted({x["group"] for x in chosen}), "tools": tl[:6], "requires": req, "missing": missing, "keys": keys,
                "asset_routes": {lib["id"]: lib["routes"][name] for lib in libs if name in lib["routes"]},
                "risks": risks or ["لا مخاطر ظاهرة من البيانات"]}

    plans = {}
    if an["level"] != "L0":
        plans = {"A": plan("A", 1, 1, 0), "B": plan("B", 2, 2, 1), "C": plan("C", 3, 2, 3)}
    # recommendation with a reason
    if an["level"] == "L0":
        rec, why = None, "طلب L0: أجب مباشرة بلا خطط"
    elif an["ambition"] == "max":
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
    brief = {"schema": "kosif.skill-intelligence.v2", "protocol": "PROTOCOL.md", "elapsed_s": None, "environment": environment(),
             "freshness": fresh, "coverage": receipt, "analysis": an, "query_terms": q[:50],
             "inventory": {"powers_total": receipt["records_on_disk"], "powers_relevant": len(relevant), "superpowers_total": len(sp.get("items", [])),
                           "superpowers_relevant": len(sp_rows), "shortlist": len(short), "groups_total": receipt["groups"], "families": receipt["families"],
                           "tools_total": readiness["summary"].get("tools"), "tools_ready": readiness["summary"].get("ready"),
                           "groups_ranked": [{"group": g, "score": round(v, 1)} for g, v in gsc.most_common()]},
             "must_have_coverage": must_cov, "excluded": excluded, "asset_libraries": libs,
             "top_powers": [{"id": r["id"], "name_ar": r["name_ar"], "name_en": r["name_en"], "group": r["group"], "catalog_status": r["status"],
                             "local_badge": local_badge(r, pres), "score": round(s, 2)} for s, r in relevant[:40]],
             "shortlist": short, "verifiers": [{"id": v["id"], "name_ar": v["name_ar"], "name_en": v["name_en"]} for v in verifiers],
             "complements": comp[:8], "tools": tools_hit[:10], "guides": guides, "plans": plans, "recommended": rec, "recommended_reason": why,
             "approval_question": (f"أنصحك بالخطة {rec}. تحب أعرض لك تفاصيل القدرات وخطوات التنفيذ، ولا توافق على الخطة ونبدأ مباشرة؟" if rec else None),
             "reply_words": {"موافق": "نفّذ الخطة الموصى بها", "تفاصيل": "جدول أعمق للقدرات والتسلسل والاعتماديات والاختبارات",
                             "A/B/C": "اعتمد خطة أخرى", "طوّر": "جولة نقد وتحسين وبحث عن تكاملات جديدة",
                             "نفّذ بأقصى قوة": "أعلى مستوى عملي دون التضحية بالاختبارات والترخيص", "نفّذ مباشرة": "تخطَّ العرض للمهام البسيطة"}}
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
    L = ["# تقرير بروتوكول ذكاء المهارات — KOSIF USIP", "", f"**المستوى {an['level']}** · **الطلب:** {an['request']}", "",
         "## بطاقة الطلب (مسودة آلية يكملها Claude)", "",
         f"- المخرج الأساسي: {an['primary']} ({', '.join(an['deliverables'])}) · الطموح: {an['ambition']}",
         f"- قيود: أرقام {an['constraints']['numbers'] or '—'} · مقاسات {an['constraints']['aspects'] or '—'} · ملفات موجودة {an['files_found'] or '—'}"
         + (" · **صوت المستخدم لا يُستبدل**" if an["constraints"]["own_assets"]["voice"] else "")
         + (" · **لقطات المستخدم لا تُستبدل**" if an["constraints"]["own_assets"]["footage"] else ""),
         "- أسئلة/افتراضات: " + (" · ".join(an["open_questions"]) or "—"), ""]
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
              f"- النمط المكتشف: {', '.join(lib['styles_detected']) or '—'} · ابحث: `{lib['command']}`",
              f"- المكان: {lib['where']}", f"- البوابة: {lib['gate']}", ""]
    pl = b["plans"]
    L += ["## مقارنة الخطط (مناهج مختلفة؛ استبدلها بمناهجك من المرحلة 4 إن كانت أقوى)", "",
          "| البند | الخطة A | الخطة B | الخطة C |", "|---|---|---|---|"]
    row = lambda label, f: L.append(f"| {label} | " + " | ".join(f(pl[k]) for k in "ABC") + " |")
    row("المنهج", lambda p: p["idea"])
    row("تغطي كل الإلزامي؟", lambda p: "نعم" if p["meets_must_haves"] else "لا: " + ", ".join(p["uncovered"])[:60])
    row("مجموعات · قدرات خارقة · قدرات مستخدمة · أدوات (جاهزة)", lambda p: f"{p['counts']['groups']} · {p['counts']['superpowers']} · {p['counts']['atoms_used']} · {p['counts']['tools']} ({p['counts']['tools_ready']})")
    row("شارات القدرات المستخدمة هنا", lambda p: " ".join(f"{k}{v}" for k, v in sorted(p["counts"]["atoms_used_local_badges"].items(), key=lambda kv: LOCAL_RANK.index(kv[0]))))
    row("متطلبات ناقصة", lambda p: str(len(p["missing"])))
    row("المخاطر", lambda p: " · ".join(p["risks"])[:150])
    if any(p.get("asset_routes") for p in pl.values()):
        row("مسار الخطوط", lambda p: " · ".join(p.get("asset_routes", {}).values())[:170] or "—")
    L += ["", "**المراحل:**"]
    for k in "ABC":
        L.append(f"- **{k}:** " + " ← ".join(f"{s}: " + ", ".join(v) for s, v in pl[k]["stages"].items()))
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
        a.out.write_text(json.dumps(br, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(summary(br, a.out))
    elif a.json:
        print(json.dumps(br, ensure_ascii=False, indent=1))
    else:
        print(render(br))
    return 0 if br["coverage"]["complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
