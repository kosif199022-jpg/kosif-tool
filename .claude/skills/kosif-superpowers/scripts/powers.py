#!/usr/bin/env python3
"""KOSIF Superpowers — search the power catalog / ابحث في قدراتك.

Python 3.8+ standard library only. Paths resolve from this file.

  python3 powers.py stats                       # counts per family and status
  python3 powers.py search glow neon            # free text (Arabic or English)
  python3 powers.py show GLOW-03                # one power in full
  python3 powers.py family light-glow-bloom     # every power in a family (stem or prefix)
  python3 powers.py suggest "دعاء هادئ بصوت رجل 9:16"   # powers + styles for a brief
  python3 powers.py styles --genre explainer    # watched reference styles
  python3 powers.py search glow --status proven ready   # filter by status
  python3 powers.py domains                     # counts per domain → family → status
  python3 powers.py mindmap [--html map.html]   # Mermaid mind map of domains → families
  python3 powers.py env [--json]                # probe this machine (runs probe_env.py)

  --domain <d>  filters search / suggest / stats (mind craft code data docs research build media strategy motion)
  --json        machine-readable output for search / show / family / suggest / stats / domains
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import unicodedata
from collections import Counter, OrderedDict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATA = ROOT / "data"
CHAPTERS = ROOT / "references" / "powers"
STATUSES = ("proven", "ready", "install", "key", "seen", "documented", "idea")
BADGE = {"proven": "✅", "ready": "🟢", "install": "📦", "key": "🔑", "seen": "👁", "documented": "📄", "idea": "💡"}
RANK = {s: i for i, s in enumerate(STATUSES)}
DEFAULT_DOMAIN = "motion"
MERMAID_CDN = "https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js"

# Domains (key → Arabic label, English label), in display order.
DOMAINS = OrderedDict([
    ("mind", ("العقل والتفكير", "Mind & thinking")),
    ("craft", ("الكتابة واللغة", "Writing & language")),
    ("code", ("الهندسة والكود", "Code & engineering")),
    ("data", ("البيانات", "Data & analysis")),
    ("docs", ("المستندات", "Documents")),
    ("research", ("البحث والويب", "Research & web")),
    ("build", ("التطبيقات والواجهات", "Apps & artifacts")),
    ("media", ("الصور والصوت", "Image & audio")),
    ("strategy", ("المنتج والمال", "Product & finance")),
    ("motion", ("الموشن والمونتاج", "Motion & video")),
])

# General families: stem → (prefix, domain, title_ar, title_en, summary_ar, summary_en).
# Motion families take their titles from the H1 of references/powers/<stem>.md.
FAMILY_META = {
    "self-discovery": ("SELF", "mind", "اكتشاف القدرات", "Self-discovery & capability inventory",
                       "اعرف ما تستطيعه فعلًا في هذه الجلسة: الأدوات والمهارات والموصلات والجهاز والشبكة.",
                       "Find out what this session can really do: tools, deferred tools, skills, connectors, machine and network."),
    "thinking-core": ("THINK", "mind", "نواة التفكير", "Thinking core",
                      "إجراءات تفكير تجعل الاستدلال أدق: التفكيك والفرضيات واختبار الافتراضات ثم القرار.",
                      "Reasoning procedures that sharpen answers: decompose, hypothesise, test assumptions, decide."),
    "creativity-engine": ("IDEA", "mind", "محرك الإبداع", "Creativity engine",
                          "توليد خيارات كثيرة متنوعة ثم اختيار الأقوى منها بمعايير واضحة.",
                          "Generate many varied options, then pick the strongest with explicit criteria."),
    "verification-evals": ("CHECK", "mind", "التحقق والتقييم", "Verification & evals",
                           "أثبت قبل أن تدّعي: اختبارات وتقييمات ومعايير قبول وإيصالات تشغيل.",
                           "Prove before claiming: tests, evals, acceptance criteria and run receipts."),
    "agent-orchestration": ("AGENT", "mind", "تنسيق الوكلاء", "Agent orchestration",
                            "تقسيم العمل على وكلاء فرعيين ومسارات متوازية ومهام مجدولة مع بوابات أمان.",
                            "Split work across subagents, parallel tracks and scheduled tasks, with safety gates."),
    "writing-humanizer": ("WRITE", "craft", "الكتابة الطبيعية", "Writing & humanizer",
                          "كتابة واضحة بصوت إنساني، وإزالة أنماط النص الآلي.",
                          "Clear writing in a human voice, and removal of machine-sounding patterns."),
    "prompt-craft": ("PROMPT", "craft", "صناعة البرومبت", "Prompt craft",
                     "كتابة البرومبت وتحسينه واختباره لنماذج النص والصورة والفيديو.",
                     "Write, improve and test prompts for text, image and video models."),
    "arabic-language": ("ARL", "craft", "اللغة العربية", "Arabic language",
                        "عربية صحيحة: الإملاء والنحو والأسلوب والتشكيل واتجاه النص.",
                        "Correct Arabic: spelling, grammar, style, diacritics and text direction."),
    "knowledge-graph": ("GRAPH", "code", "الرسم المعرفي والخرائط الذهنية", "Knowledge graph & mind maps",
                        "حوّل الكود والمستندات والأفكار إلى رسوم معرفية وخرائط ذهنية يمكن الاستعلام عنها.",
                        "Turn code, documents and ideas into queryable knowledge graphs and mind maps."),
    "code-engineering": ("CODE", "code", "هندسة البرمجيات", "Code engineering",
                         "كتابة الكود وتصحيحه ومراجعته واختباره وتسليمه بأمان.",
                         "Write, debug, review, test and ship code safely."),
    "security-safety": ("SEC", "code", "الأمان والسلامة", "Security & safety",
                        "مراجعة الثغرات وحماية الأسرار والمدخلات غير الموثوقة وبوابات الأفعال الخطرة.",
                        "Vulnerability review, secret hygiene, untrusted input and gates for risky actions."),
    "data-analysis": ("ANLY", "data", "تحليل البيانات", "Data analysis",
                      "تحميل البيانات وتنظيفها وتحليلها واختبار الفرضيات وتلخيصها برسوم صادقة.",
                      "Load, clean, analyse and test data, then summarise it with honest charts."),
    "documents-office": ("DOC", "docs", "المستندات والمكتب", "Documents & office",
                         "إنشاء ملفات وورد وإكسل وباوربوينت وPDF وتحويلها واستخراج محتواها.",
                         "Create, convert and extract Word, Excel, PowerPoint and PDF files."),
    "web-research": ("WEB", "research", "البحث على الويب", "Web research",
                     "البحث في المصادر وقراءتها والاستشهاد بها والتحقق من المعلومات.",
                     "Search, read, cite and fact-check sources on the web."),
    "apps-artifacts": ("APP", "build", "التطبيقات والواجهات", "Apps & artifacts",
                       "بناء صفحات وتطبيقات ولوحات تفاعلية ومعاينتها ونشرها.",
                       "Build, preview and publish interactive pages, apps and dashboards."),
    "media-image-audio": ("MEDIA", "media", "الصور والصوت", "Image & audio",
                          "معالجة الصور والصوت: التحويل والقص وقراءة النص من الصور والتفريغ والتوليد.",
                          "Process images and audio: convert, crop, OCR, transcribe and generate."),
    "strategy-finance": ("PROD", "strategy", "المنتج والاستراتيجية والمال", "Product, strategy & finance",
                         "خطط المنتجات والتسعير والاستراتيجية والنماذج المالية بأرقام قابلة للتحقق.",
                         "Product plans, pricing, strategy and financial models with checkable numbers."),
}

# Arabic/English intent words → extra search terms, so a brief written in
# plain words still reaches the right families. Special tokens in a value:
#   "@PREFIX" boosts that family (e.g. "@ANLY"), "~domain" boosts that domain,
#   "!hint" adds a hint line to `suggest`. Keys with spaces match the whole brief.
INTENT = {
    "دعاء": ["calm", "arabic", "calligraphy", "glow", "particles", "slow", "~motion"],
    "قرآن": ["calm", "arabic", "calligraphy", "no-music", "glow", "~motion"],
    "شعر": ["kinetic", "arabic", "calligraphy", "typography"],
    "أغنية": ["beat", "lyrics", "karaoke", "music", "~motion"],
    "اغنية": ["beat", "lyrics", "karaoke", "music", "~motion"],
    "موسيقى": ["beat", "audio-reactive", "music", "~motion"],
    "إعلان": ["ad", "product", "hook", "cta", "logo", "~motion"],
    "اعلان": ["ad", "product", "hook", "cta", "logo", "~motion"],
    "منتج": ["product", "ui", "phone", "3d", "@PROD"],
    "تطبيق": ["app", "ui", "phone", "cursor", "@APP"],
    "بيانات": ["chart", "counter", "data", "infographic", "@ANLY"],
    "أرقام": ["chart", "counter", "data"],
    "خريطة": ["map", "route", "geo"],
    "تعليمي": ["explainer", "diagram", "whiteboard"],
    "شرح": ["explainer", "diagram", "whiteboard"],
    "أطفال": ["character", "cartoon", "playful"],
    "قصة": ["story", "character", "narrative"],
    "بودكاست": ["podcast", "captions", "waveform", "talking-head", "~motion"],
    "مونتاج": ["montage", "cuts", "transitions", "ffmpeg", "grade", "~motion"],
    "ريلز": ["9:16", "reel", "captions", "hook", "~motion"],
    "توهج": ["glow", "bloom", "neon", "~motion"],
    "نيون": ["neon", "glow", "~motion"],
    "خط": ["typography", "font"],
    "ألوان": ["palette", "color", "grade"],
    "ثلاثي": ["3d", "three"],
    "هادئ": ["calm", "slow", "ease"],
    "سريع": ["fast", "beat", "punch"],
    "فخم": ["luxury", "gold", "serif"],
}
# the first table above keeps its original loose substring match (except the
# two-letter "خط", which must not fire on "خطة" plan or "مخطط" chart)
_LEGACY_KEYS = set(INTENT) - {"خط"}
INTENT.update({
    # motion signals (domain boost)
    "فيديو": ["video", "~motion"], "موشن": ["motion", "~motion"], "انميشن": ["animation", "~motion"],
    "انيميشن": ["animation", "~motion"], "رسوم متحركة": ["animation", "~motion"],
    "video": ["~motion"], "motion": ["~motion"], "animation": ["~motion"], "animate": ["animation", "~motion"],
    "reel": ["~motion"], "reels": ["reel", "~motion"], "montage": ["~motion"], "captions": ["~motion"],
    "subtitles": ["captions", "~motion"], "kinetic": ["~motion"], "mp4": ["render", "~motion"],
    "9:16": ["~motion"], "16:9": ["~motion"], "1:1": ["~motion"], "4:5": ["~motion"],
    "tiktok": ["9:16", "~motion"], "تيك توك": ["9:16", "~motion"], "youtube": ["~motion"], "يوتيوب": ["~motion"],
    # data analysis
    "تحليل": ["analysis", "data", "@ANLY"], "حلل": ["analysis", "data", "@ANLY"], "إحصاء": ["statistics", "@ANLY"],
    "csv": ["csv", "pandas", "data", "@ANLY"], "analysis": ["@ANLY"], "analyse": ["analysis", "@ANLY"],
    "analyze": ["analysis", "@ANLY"], "dataset": ["data", "@ANLY"], "statistics": ["@ANLY"],
    "sql": ["sql", "duckdb", "@ANLY"], "pandas": ["@ANLY"], "spreadsheet data": ["@ANLY", "@DOC"],
    # documents & office
    "مستند": ["document", "docx", "@DOC"], "وورد": ["docx", "word", "@DOC"], "pdf": ["pdf", "@DOC"],
    "إكسل": ["xlsx", "excel", "@DOC"], "اكسيل": ["xlsx", "excel", "@DOC"], "excel": ["xlsx", "@DOC"],
    "docx": ["@DOC"], "xlsx": ["@DOC"], "pptx": ["@DOC"], "powerpoint": ["pptx", "@DOC"],
    "بوربوينت": ["pptx", "@DOC"], "باوربوينت": ["pptx", "@DOC"], "عرض تقديمي": ["pptx", "slides", "@DOC"],
    "تقرير": ["report", "@DOC"], "report": ["@DOC"], "document": ["@DOC"], "word document": ["docx", "@DOC"],
    "spreadsheet": ["xlsx", "@DOC"],
    # web research
    "بحث": ["research", "search", "@WEB"], "ابحث": ["research", "search", "@WEB"],
    "مصادر": ["sources", "citations", "@WEB"], "research": ["@WEB"], "sources": ["citations", "@WEB"],
    "cite": ["citations", "@WEB"], "citations": ["@WEB"], "scrape": ["scraping", "@WEB"], "scraping": ["@WEB"],
    "crawl": ["scraping", "@WEB"], "web search": ["@WEB"], "fact check": ["@WEB", "@CHECK"], "إنترنت": ["web", "@WEB"],
    # code
    "كود": ["code", "@CODE"], "برمج": ["code", "programming", "@CODE"], "bug": ["debug", "@CODE"],
    "debug": ["@CODE"], "refactor": ["@CODE"], "code": ["@CODE"], "coding": ["code", "@CODE"],
    "programming": ["code", "@CODE"], "pull request": ["github", "@CODE"], "repo": ["github", "@CODE"],
    "github": ["@CODE"], "unit test": ["tests", "@CODE", "@CHECK"], "مراجعة كود": ["review", "@CODE", "@CHECK"],
    # writing, prompts, ideas, Arabic language
    "اكتب": ["write", "@WRITE"], "مقال": ["article", "@WRITE"], "صياغة": ["rewrite", "@WRITE"],
    "كتابة": ["write", "@WRITE"], "write": ["@WRITE"], "article": ["@WRITE"], "essay": ["@WRITE"],
    "rewrite": ["@WRITE"], "humanize": ["@WRITE"], "blog": ["article", "@WRITE"], "email": ["@WRITE"],
    "إيميل": ["email", "@WRITE"], "copywriting": ["@WRITE"],
    "برومبت": ["prompt", "@PROMPT"], "برومت": ["prompt", "@PROMPT"], "prompt": ["@PROMPT"],
    "prompts": ["prompt", "@PROMPT"], "system prompt": ["@PROMPT"],
    "فكرة": ["ideas", "@IDEA"], "أفكار": ["ideas", "@IDEA"], "إبداع": ["creative", "@IDEA"],
    "عصف ذهني": ["brainstorm", "@IDEA"], "idea": ["@IDEA"], "ideas": ["@IDEA"], "brainstorm": ["@IDEA"],
    "creative": ["@IDEA"],
    "إملاء": ["spelling", "@ARL"], "إعراب": ["grammar", "@ARL"], "تدقيق لغوي": ["proofread", "@ARL"],
    "قواعد اللغة": ["grammar", "@ARL"], "grammar": ["@ARL", "@WRITE"], "proofread": ["@ARL", "@WRITE"],
    "فصحى": ["@ARL"], "لهجة": ["dialect", "@ARL"],
    # self-discovery
    "قدراتك": ["capabilities", "@SELF", "!self"], "قدراتي": ["capabilities", "@SELF", "!self"],
    "مهاراتك": ["skills", "@SELF", "!self"], "تقدر تعمل ايه": ["@SELF", "!self"],
    "تقدر تسوي ايش": ["@SELF", "!self"], "وش تقدر": ["@SELF", "!self"], "ماذا تستطيع": ["@SELF", "!self"],
    "what can you do": ["@SELF", "!self"], "capabilities": ["@SELF", "!self"], "your skills": ["@SELF", "!self"],
    "superpowers": ["@SELF", "!self"],
    # apps & artifacts
    "موقع": ["website", "@APP"], "داشبورد": ["dashboard", "@APP"], "لوحة تحكم": ["dashboard", "@APP"],
    "صفحة هبوط": ["landing", "@APP"], "dashboard": ["@APP"], "website": ["@APP"], "web app": ["@APP"],
    "webapp": ["@APP"], "landing page": ["@APP"], "artifact": ["@APP"], "app": ["@APP"],
    # media
    "صورة": ["image", "@MEDIA"], "صور": ["image", "@MEDIA"], "صوت": ["audio", "@MEDIA"], "ocr": ["@MEDIA", "@DOC"],
    "image": ["@MEDIA"], "audio": ["@MEDIA"], "transcribe": ["transcription", "@MEDIA"],
    "transcript": ["transcription", "@MEDIA"], "تفريغ": ["transcription", "@MEDIA"],
    "remove background": ["@MEDIA"], "إزالة الخلفية": ["background", "@MEDIA"],
    # product, strategy & finance
    "خطة": ["plan", "@PROD"], "تسعير": ["pricing", "@PROD"], "pricing": ["@PROD"], "roadmap": ["@PROD"],
    "strategy": ["@PROD"], "استراتيجية": ["strategy", "@PROD"], "business plan": ["@PROD"],
    "ميزانية": ["budget", "@PROD"], "budget": ["@PROD"], "finance": ["@PROD"], "financial": ["finance", "@PROD"],
    "تمويل": ["finance", "@PROD"], "إيرادات": ["revenue", "@PROD"], "أرباح": ["profit", "@PROD"],
    "نموذج مالي": ["finance", "@PROD"], "prd": ["@PROD"], "دراسة جدوى": ["@PROD"],
    # security
    "أمان": ["security", "@SEC"], "ثغرة": ["vulnerability", "@SEC"], "ثغرات": ["vulnerability", "@SEC"],
    "اختراق": ["security", "@SEC"], "حماية": ["security", "@SEC"], "security": ["@SEC"], "vulnerability": ["@SEC"],
    "vuln": ["vulnerability", "@SEC"], "secrets": ["@SEC"], "prompt injection": ["@SEC", "@PROMPT"],
    "threat model": ["@SEC"], "cve": ["@SEC"],
    # knowledge graph & mind maps
    "خريطة ذهنية": ["mindmap", "mermaid", "@GRAPH", "!mindmap"], "خرائط ذهنية": ["mindmap", "@GRAPH", "!mindmap"],
    "mind map": ["mindmap", "@GRAPH", "!mindmap"], "mindmap": ["@GRAPH", "!mindmap"],
    "knowledge graph": ["@GRAPH"], "graphify": ["@GRAPH"],
    # thinking, verification, agents
    "تفكير": ["thinking", "@THINK"], "قرار": ["decision", "@THINK"], "decision": ["@THINK"],
    "reasoning": ["@THINK"], "think": ["@THINK"], "thinking": ["@THINK"], "premortem": ["@THINK"],
    "تحقق": ["verify", "@CHECK"], "verify": ["@CHECK"], "verification": ["@CHECK"], "evals": ["@CHECK"],
    "eval": ["@CHECK"], "تقييم": ["evaluation", "@CHECK"],
    "وكلاء": ["agents", "@AGENT"], "وكيل": ["agent", "@AGENT"], "subagent": ["@AGENT"], "orchestrate": ["@AGENT"],
    "orchestration": ["@AGENT"], "parallel": ["@AGENT"], "workflow": ["@AGENT"], "جدولة": ["schedule", "@AGENT"],
    "schedule": ["@AGENT"], "automation": ["@AGENT"], "أتمتة": ["automation", "@AGENT"],
})
_EXACT_KEYS = {"excel", "motion", "think", "sources"}  # ASCII keys that must not match inside longer words
_AR_PREFIXES = ("وبال", "فبال", "وال", "بال", "فال", "كال", "لل", "ال", "و", "ف", "ب", "ل", "ك")
_AR_SUFFIXES = ("", "ي", "ات", "ين", "ون", "وط", "ها", "هم")
HINTS = {
    "self": "self-map: python3 scripts/powers.py domains · python3 scripts/powers.py mindmap --html map.html · python3 scripts/powers.py env",
    "mindmap": "mind map: python3 scripts/powers.py mindmap --html mindmap.html draws this catalog; for the user's topic write a Mermaid `mindmap` the same way",
}


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s or "").lower()
    s = re.sub(r"[ً-ْـ]", "", s)  # tashkeel and tatweel
    return s.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا").replace("ة", "ه").replace("ى", "ي")


# function words dropped from a brief before scoring (they match inside unrelated words)
STOP = {norm(w) for w in (
    "في من على إلى الى عن مع هذا هذه ذلك تلك التي الذي اللي و أو او ثم لي لك لنا ايش إيش ايه إيه وش شو كيف ماذا "
    "ما هل أنا انا أنت انت عندي اعمل اعطني أعطني ابغى ابي أبي ممكن لو سمحت عشان علشان بس كل بعض يا "
    "the a an and or to of for in on at by my me this that these those with please can could you your i is are "
    "it be do does make some any want need how what which from into").split()}


def load_powers() -> list:
    out = []
    for p in sorted((DATA / "powers").glob("*.json")):
        try:
            rows = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            print(f"warning: {p.name}: {e}", file=sys.stderr)
            continue
        if not isinstance(rows, list):
            print(f"warning: {p.name}: expected a JSON list, skipped", file=sys.stderr)
            continue
        for r in rows:
            if isinstance(r, dict):
                if not r.get("domain"):
                    r["domain"] = DEFAULT_DOMAIN
                out.append(r)
    return out


def load_styles() -> list:
    p = DATA / "styles.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else []


_TEXT = {}


def text_of(p: dict) -> str:
    key = id(p)
    if key not in _TEXT:
        keys = ("id", "family", "name_ar", "name_en", "what", "when", "how", "params", "tags", "styles", "section")
        _TEXT[key] = norm(" ".join(json.dumps(p.get(k) or "", ensure_ascii=False) for k in keys))
    return _TEXT[key]


def score(p: dict, terms: list) -> float:
    t = text_of(p)
    name = norm(f"{p.get('name_ar', '')} {p.get('name_en', '')} {' '.join(p.get('tags') or [])}")
    s = 0.0
    for w in terms:
        if w[:1] in ("@", "~", "!"):
            continue
        w = norm(w)
        if not w:
            continue
        hits = t.count(w)
        if hits:
            s += 1 + min(hits, 5) * 0.3 + (2 if w in name else 0)
    return s - RANK.get(p.get("status"), 6) * 0.05  # prefer proven/ready on ties


def line(p: dict) -> str:
    return f"{p.get('id', '?'):<10} {BADGE.get(p.get('status'), '·')} {p.get('name_ar', '')} — {p.get('name_en', '')}"


def prefix_of(p: dict) -> str:
    m = re.match(r"^([A-Za-z0-9]+)-", str(p.get("id", "")))
    return m.group(1).upper() if m else ""


def _key_matches(key: str, nk: str, nw: str) -> bool:
    ascii_key = all(ord(ch) < 128 for ch in nk)
    if key in _LEGACY_KEYS or (len(nk) >= 4 and not ascii_key) or (ascii_key and len(nk) >= 5 and nk not in _EXACT_KEYS):
        return nk in nw
    if ascii_key:
        return nw == nk or nw == nk + "s"
    for pre in ("",) + _AR_PREFIXES:  # short Arabic key: whole word with clitics
        if pre and not nw.startswith(pre):
            continue
        stem = nw[len(pre):]
        if any(stem == nk + suf for suf in _AR_SUFFIXES):
            return True
    return False


def expand(words: list, brief: str = "") -> list:
    """Words + intent terms. Special tokens (@FAMILY, ~domain, !hint) ride along."""
    out = list(words)
    joined = " " + " ".join(norm(w) for w in re.findall(r"[\w:]+", brief or " ".join(words))) + " "
    multi = [k for k in INTENT if " " in k and " " + norm(k) + " " in joined]
    for k in multi:
        out += INTENT[k]
    multi_n = [norm(k) for k in multi]
    for w in words:
        nw = norm(w)
        for k, extra in INTENT.items():
            if " " in k:
                continue
            nk = norm(k)
            if any(nk in m for m in multi_n):
                continue
            if _key_matches(k, nk, nw):
                out += extra
    return out


def intent_of(terms: list):
    fam = Counter(t[1:].upper() for t in terms if t.startswith("@"))
    dom = Counter(t[1:] for t in terms if t.startswith("~"))
    hints = list(OrderedDict.fromkeys(t[1:] for t in terms if t.startswith("!")))
    return fam, dom, hints


def rank(powers: list, terms: list, inject: bool):
    """Score every power: text match + family/domain intent boosts.

    inject=True lets an intent-named family appear even without a text hit
    (suggest); inject=False only re-ranks text matches (search)."""
    fam, dom, _ = intent_of(terms)
    motion_ctx = dom.get("motion", 0) > 0
    out = []
    for p in powers:
        base = score(p, terms)
        bonus = 0.0
        hit = min(fam.get(prefix_of(p), 0), 3)
        if hit:
            if not inject or (motion_ctx and p.get("domain") != "motion"):
                bonus = 1.0 * hit if base > 0 else 0.0
            else:
                bonus = 3.0 * hit
        if base > 0 and dom.get(p.get("domain")):
            bonus += 1.5
        total = base + bonus
        if total > 0 and (base > 0 or bonus > 0):
            out.append((total, p))
    out.sort(key=lambda x: -x[0])
    return out


# ------------------------------------------------------------------ titles & families

_TITLES = {}


def family_title(stem: str):
    """(title_ar, title_en) from FAMILY_META or the chapter H1 '# AR — EN'."""
    if stem in _TITLES:
        return _TITLES[stem]
    t = (stem, stem)
    if stem in FAMILY_META:
        t = (FAMILY_META[stem][2], FAMILY_META[stem][3])
    else:
        f = CHAPTERS / f"{stem}.md"
        try:
            with f.open(encoding="utf-8") as fh:
                first = fh.readline().strip().lstrip("#").strip()
            if " — " in first:
                ar, en = first.split(" — ", 1)
                t = (ar.strip(), en.strip())
            elif first:
                t = (first, stem)
        except OSError:
            pass
    _TITLES[stem] = t
    return t


def families(powers: list):
    """OrderedDict stem → {prefix, domain, count, status Counter} in domain order."""
    info = {}
    for p in powers:
        f = p.get("family") or "?"
        d = info.setdefault(f, {"prefixes": Counter(), "domains": Counter(), "status": Counter(), "count": 0})
        d["prefixes"][prefix_of(p)] += 1
        d["domains"][p.get("domain") or DEFAULT_DOMAIN] += 1
        d["status"][p.get("status")] += 1
        d["count"] += 1
    order = {k: i for i, k in enumerate(DOMAINS)}
    rows = []
    for f, d in info.items():
        dom = d["domains"].most_common(1)[0][0]
        pre = FAMILY_META[f][0] if f in FAMILY_META else d["prefixes"].most_common(1)[0][0]
        rows.append((order.get(dom, 99), dom, -d["count"], f, {"family": f, "prefix": pre, "domain": dom,
                                                            "count": d["count"], "status": d["status"]}))
    rows.sort(key=lambda r: r[:4])
    return OrderedDict((r[3], r[4]) for r in rows)


def status_str(st: Counter, compact: bool = True) -> str:
    if compact:
        return " ".join(f"{BADGE[s]}{st[s]}" for s in STATUSES if st.get(s))
    return "  ".join(f"{BADGE[s]} {s} {st.get(s, 0)}" for s in STATUSES)


def best_badge(st: Counter) -> str:
    for s in STATUSES:
        if st.get(s):
            return f"{BADGE[s]}{st[s]}"
    return ""


def short(p: dict, s: float = None) -> dict:
    d = {k: p.get(k) for k in ("id", "family", "domain", "status", "name_ar", "name_en")}
    d["badge"] = BADGE.get(p.get("status"), "·")
    if s is not None:
        d["score"] = round(s, 3)
    return d


def emit(obj) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=1))


# ------------------------------------------------------------------ verbs

def by_domain(powers, a):
    d = getattr(a, "domain", None)
    if d:
        powers = [p for p in powers if (p.get("domain") or DEFAULT_DOMAIN) == d]
    return powers


def check_domain(powers, a) -> bool:
    d = getattr(a, "domain", None)
    known = set(DOMAINS) | {p.get("domain") for p in powers}
    if d and d not in known:
        print(f"unknown domain {d} — domains: {', '.join(k for k in DOMAINS)}", file=sys.stderr)
        return False
    return True


def cmd_stats(powers, styles, a) -> int:
    if not check_domain(powers, a):
        return 2
    powers = by_domain(powers, a)
    fam = Counter(p.get("family") for p in powers)
    st = Counter(p.get("status") for p in powers)
    dom = Counter(p.get("domain") for p in powers)
    watched = sum(1 for s in styles if s.get("watched"))
    if getattr(a, "json", False):
        emit({"powers": len(powers), "families": len(fam), "domains": dict(dom), "watched_styles": watched,
              "styles": len(styles), "status": {s: st.get(s, 0) for s in STATUSES}, "by_family": dict(fam.most_common())})
        return 0
    print(f"powers: {len(powers)} · families: {len(fam)} · watched styles: {watched}")
    print("status: " + "  ".join(f"{BADGE[s]} {s} {st.get(s, 0)}" for s in STATUSES))
    for f, n in fam.most_common():
        print(f"  {n:4d}  {f}")
    print("domains: " + " · ".join(f"{d} {dom[d]}" for d in list(DOMAINS) + sorted(set(dom) - set(DOMAINS)) if dom.get(d)))
    return 0


def filtered(powers, a):
    if getattr(a, "status", None):
        powers = [p for p in powers if p.get("status") in a.status]
    return by_domain(powers, a)


def cmd_search(powers, _styles, a) -> int:
    if not check_domain(powers, a):
        return 2
    terms = expand(a.words)
    ranked = rank(filtered(powers, a), terms, inject=False)[: a.limit]
    if getattr(a, "json", False):
        emit([short(p, s) for s, p in ranked])
        return 0 if ranked else 1
    if not ranked:
        print("no match / لا نتائج")
        return 1
    for _s, p in ranked:
        print(line(p))
    return 0


SHOW_KEYS = ("id", "family", "domain", "name_ar", "name_en", "status", "what", "when", "how", "params", "install",
             "license", "proof", "styles", "tags", "section", "source")


def cmd_show(powers, _styles, a) -> int:
    want = a.id.upper()
    for p in powers:
        if str(p.get("id", "")).upper() == want:
            if getattr(a, "json", False):
                emit(p)
                return 0
            for k in SHOW_KEYS:
                v = p.get(k)
                if v:
                    print(f"{k}: {v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)}")
            return 0
    if getattr(a, "json", False):
        emit({"error": f"unknown power id {a.id}"})
    else:
        print(f"unknown power id {a.id}")
    return 1


def cmd_family(powers, _styles, a) -> int:
    rows = [p for p in filtered(powers, a) if p.get("family") == a.family]
    if not rows:  # accept a prefix such as GLOW or ANLY
        rows = [p for p in filtered(powers, a) if prefix_of(p) == a.family.upper()]
    if getattr(a, "json", False):
        emit([short(p) for p in rows] if rows else {"error": f"unknown family {a.family}",
                                                     "families": sorted({p.get('family') for p in powers})})
        return 0 if rows else 1
    if not rows:
        print("families: " + ", ".join(sorted({p.get('family') for p in powers})))
        return 1
    for p in rows:
        print(line(p))
    return 0


def suggest(powers, styles, brief: str, limit: int = 18, domain: str = None) -> dict:
    """Rank powers for a brief across all domains (or one). Used by `suggest` and by evals."""
    words = expand(re.findall(r"[\w:]+", brief), brief)
    words = [w for w in words if w[:1] in "@~!" or (len(norm(w)) >= 2 and norm(w) not in STOP)]
    fam_i, dom_i, hints = intent_of(words)
    general = {m[0] for m in FAMILY_META.values()}
    general_intent = any(f in general for f in fam_i)
    pool = [p for p in powers if not domain or (p.get("domain") or DEFAULT_DOMAIN) == domain]
    picked, fams = [], Counter()
    for s, p in rank(pool, words, inject=True):
        if len(picked) >= limit:
            break
        cap = 5 if (general_intent and not dom_i.get("motion") and prefix_of(p) in fam_i) else 3
        if fams[p.get("family")] >= cap:  # spread across families
            continue
        fams[p.get("family")] += 1
        picked.append((s, p))
    motion_share = sum(1 for _s, p in picked if p.get("domain") == "motion") / max(1, len(picked))
    motion_out = domain == "motion" or (not domain and bool(
        dom_i.get("motion") or (not general_intent and motion_share >= 0.5)))
    st = []
    if motion_out and styles:
        st = sorted(styles, key=lambda s: -sum(norm(json.dumps(s, ensure_ascii=False)).count(norm(w))
                                               for w in words if w[:1] not in "@~!"))[:8]
    aspect = re.search(r"\b(9:16|16:9|1:1|4:5)\b", brief)
    return {"brief": brief, "domain_filter": domain, "picked": picked, "styles": st, "motion": motion_out,
            "intent": {"families": dict(fam_i), "domains": dict(dom_i)}, "hints": hints,
            "chapters": list(OrderedDict.fromkeys(p.get("family") for _s, p in picked)),
            "format": (aspect.group(1) if aspect else "9:16 default") if motion_out else None}


def cmd_suggest(powers, styles, a) -> int:
    if not check_domain(powers, a):
        return 2
    brief = " ".join(a.brief)
    r = suggest(powers, styles, brief, a.limit, getattr(a, "domain", None))
    picked, st, chapters, hints = r["picked"], r["styles"], r["chapters"], r["hints"]
    if getattr(a, "json", False):
        emit({"brief": brief, "domain_filter": r["domain_filter"], "intent": r["intent"],
              "powers": [short(p, s) for s, p in picked],
              "styles": [{"id": s.get("id"), "title_ar": s.get("title_ar"), "proves_ar": s.get("proves_ar")} for s in st],
              "chapters": [f"references/powers/{f}.md" for f in chapters], "format": r["format"],
              "hints": [HINTS[h] for h in hints if h in HINTS]})
        return 0
    print(f"# powers for: {brief}")
    for _s, p in picked:
        print(line(p))
    if r["motion"]:
        if st:
            print("\n# reference styles to study")
            for s in st:
                print(f"{s.get('id'):<28} {s.get('title_ar', '')} — {s.get('proves_ar', '')}"[:160])
        print(f"\nformat: {r['format']} · then: python3 tools/kosif.py scaffold <style> <dir>")
    else:
        print("\n# chapters to open")
        for f in chapters:
            exists = (CHAPTERS / f"{f}.md").is_file()
            print(f"references/powers/{f}.md" + ("" if exists else "  (not generated yet: python3 scripts/build_chapters.py)"))
        print("\nnext: python3 scripts/powers.py show <ID> · machine check: python3 scripts/powers.py env")
    for h in hints:
        if h in HINTS:
            print(HINTS[h])
    return 0


def cmd_styles(_powers, styles, a) -> int:
    rows = [s for s in styles if not a.genre or norm(a.genre) in norm(s.get("genre", ""))]
    for s in rows[: a.limit]:
        print(f"{s.get('id'):<28} {s.get('genre', ''):<16} {s.get('title_ar', '')}")
    return 0 if rows else 1


def cmd_domains(powers, _styles, a) -> int:
    fams = families(powers)
    dom_rows = OrderedDict()
    for f, d in fams.items():
        r = dom_rows.setdefault(d["domain"], {"count": 0, "status": Counter(), "families": []})
        r["count"] += d["count"]
        r["status"].update(d["status"])
        r["families"].append(d)
    if getattr(a, "json", False):
        emit({"powers": len(powers), "families": len(fams), "domains": OrderedDict(
            (k, {"label_ar": DOMAINS.get(k, (k, k))[0], "label_en": DOMAINS.get(k, (k, k))[1], "count": r["count"],
                 "status": {s: r["status"].get(s, 0) for s in STATUSES},
                 "families": [{"family": d["family"], "prefix": d["prefix"], "count": d["count"],
                               "title_ar": family_title(d["family"])[0], "title_en": family_title(d["family"])[1],
                               "status": {s: d["status"].get(s, 0) for s in STATUSES}} for d in r["families"]]})
            for k, r in dom_rows.items())})
        return 0
    print(f"domains: {len(dom_rows)} · families: {len(fams)} · powers: {len(powers)}")
    for k, r in dom_rows.items():
        ar, en = DOMAINS.get(k, (k, k))
        print(f"\n{k:<9} {ar} — {en}  ·  {r['count']}  ·  {status_str(r['status'])}")
        for d in r["families"]:
            print(f"  {d['prefix']:<7} {d['family']:<28} {d['count']:5d}  {status_str(d['status'])}")
    missing = [k for k in DOMAINS if k not in dom_rows]
    if missing:
        print("\nno powers yet: " + ", ".join(missing))
    return 0


# motion is big: the mind map groups its 30 families into 8 branches (prefix lists)
MOTION_GROUPS = OrderedDict([
    ("type", ("النص والخط", "Type & lettering", ("ARAB", "TYPE"))),
    ("look", ("اللون والضوء والملمس", "Colour, light & texture", ("COLOR", "GLOW", "TEX", "RETRO"))),
    ("move", ("الشكل والحركة", "Shape & movement", ("SHAPE", "PART", "EASE", "DRAW", "CHAR"))),
    ("camera", ("الكاميرا والقطع", "Camera & cuts", ("CAM", "TRANS", "3D"))),
    ("sound", ("الصوت والتزامن", "Sound & sync", ("SYNC", "BEAT", "VOICE"))),
    ("content", ("المحتوى والشرح", "Content & explainers", ("DATA", "MAP", "EXPL", "UI", "BRAND", "FOOT"))),
    ("story", ("القصة والمنصات", "Story & formats", ("STORY", "FMT"))),
    ("pipeline", ("الأدوات والجودة", "Pipeline & QA", ("ENG", "QA", "GEN", "DL", "MISC"))),
])


def _mm(text: str) -> str:
    """Make text safe inside a Mermaid mindmap node label."""
    text = re.sub(r"[()\[\]{}<>\"`]", " ", str(text)).replace("&", "and")
    return re.sub(r"\s+", " ", text).strip()


def _motion_group(prefix: str) -> str:
    for k, (_ar, _en, pres) in MOTION_GROUPS.items():
        if prefix in pres:
            return k
    return "other"


def mindmap_source(powers, a) -> str:
    en = getattr(a, "en", False)
    fams = families(powers)
    drill = getattr(a, "domain", None)
    top = max(0, getattr(a, "top", 5))
    lines = ["mindmap"]
    n_id = [0]

    def node(depth: int, label, shape: str = "[]") -> None:
        """label = (title, facts): two lines so Arabic text and numbers never share a bidi run."""
        n_id[0] += 1
        title, facts = label
        lines.append("  " * depth + f'n{n_id[0]}{shape[0]}"`{_mm(facts)}\n{_mm(title)}`"{shape[1:]}')

    def fam_label(d):
        t_ar, t_en = family_title(d["family"])
        return (t_en if en else t_ar, f"{d['prefix']} · {d['count']} · {best_badge(d['status'])}")

    def dom_label(dom: str, rows):
        ar, e = DOMAINS.get(dom, (dom, dom))
        st = Counter()
        for x in rows:
            st.update(x["status"])
        return (e if en else ar, f"{sum(x['count'] for x in rows)} · {best_badge(st)}")

    def powers_of(fam: str, depth: int) -> None:
        rows = sorted((p for p in powers if p.get("family") == fam), key=lambda p: (RANK.get(p.get("status"), 9), str(p.get("id"))))
        for p in rows[:top]:
            node(depth, (p.get("name_en") if en else p.get("name_ar"), f"{p.get('id')} {BADGE.get(p.get('status'), '')}"))

    def families_of(dom: str, rows, depth: int) -> None:
        if dom == "motion":
            groups = OrderedDict()
            for d in rows:
                groups.setdefault(_motion_group(d["prefix"]), []).append(d)
            order = list(MOTION_GROUPS) + ["other"]
            for g in sorted(groups, key=order.index):
                ar, e, _p = MOTION_GROUPS.get(g, ("أخرى", "Other", ()))
                node(depth, (e if en else ar, str(sum(x["count"] for x in groups[g]))), "()")
                for d in groups[g]:
                    node(depth + 1, fam_label(d))
                    if drill:
                        powers_of(d["family"], depth + 2)
            return
        for d in rows:
            node(depth, fam_label(d))
            if drill:
                powers_of(d["family"], depth + 1)

    by_dom = OrderedDict()
    for d in fams.values():
        by_dom.setdefault(d["domain"], []).append(d)
    if drill:
        rows = by_dom.get(drill, [])
        t, f = dom_label(drill, rows)
        lines.append(f'  root(("`{_mm(f)}\n{_mm(t)}`"))')
        families_of(drill, rows, 2)
    else:
        lines.append(f"  root((Kosif superpowers · {len(powers)}))")
        for dom, rows in by_dom.items():
            node(2, dom_label(dom, rows))
            families_of(dom, rows, 3)
    return "\n".join(lines) + "\n"


def mindmap_html(src: str, powers, a) -> str:
    fams = families(powers)
    items = []
    cur = None
    for f, d in fams.items():
        if getattr(a, "domain", None) and d["domain"] != a.domain:
            continue
        if d["domain"] != cur:
            if cur is not None:
                items.append("</ul></li>")
            cur = d["domain"]
            ar, en = DOMAINS.get(cur, (cur, cur))
            n = sum(x["count"] for x in fams.values() if x["domain"] == cur)
            items.append(f"<li><strong>{html.escape(ar)} — {html.escape(en)}</strong> · {n}<ul>")
        t_ar, t_en = family_title(f)
        items.append(f"<li><code>{html.escape(d['prefix'])}</code> {html.escape(t_ar)} — {html.escape(t_en)} · "
                     f"{d['count']} · {html.escape(status_str(d['status']))}</li>")
    if cur is not None:
        items.append("</ul></li>")
    total = sum(d["count"] for d in fams.values() if not getattr(a, "domain", None) or d["domain"] == a.domain)
    return f"""<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Capability mind map</title>
<style>
:root {{ --bg:#f7f6f2; --fg:#1d1d1f; --muted:#5f5f66; --card:#ffffff; --line:#e2e0da; --accent:#0f6e6e; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#121214; --fg:#ececef; --muted:#a1a1aa; --card:#1b1b1f; --line:#2c2c33; --accent:#5cc8c8; }} }}
* {{ box-sizing: border-box; }}
body {{ margin:0; background:var(--bg); color:var(--fg); font:15px/1.6 system-ui, -apple-system, "Segoe UI", "Noto Sans Arabic", Tahoma, sans-serif; }}
main {{ max-width:1280px; margin:0 auto; padding:24px 16px 48px; }}
h1 {{ font-size:1.5rem; margin:0 0 4px; }}
.meta {{ color:var(--muted); margin:0 0 16px; }}
.card {{ background:var(--card); border:1px solid var(--line); border-radius:12px; padding:12px; overflow:auto; }}
#diagram svg {{ max-width:100%; height:auto; }}
#diagram.actual svg {{ max-width:none !important; }}
.tools {{ margin:8px 0; }}
button {{ font:inherit; color:var(--accent); background:var(--card); border:1px solid var(--line); border-radius:8px; padding:4px 10px; cursor:pointer; }}
#note {{ color:var(--muted); font-size:.9rem; margin:8px 0 0; }}
details {{ margin-top:16px; }}
summary {{ cursor:pointer; color:var(--accent); font-weight:600; }}
ul {{ padding-inline-start:1.2rem; }}
code {{ background:var(--bg); border:1px solid var(--line); border-radius:4px; padding:0 4px; }}
</style>
</head>
<body>
<main>
<h1>خريطة القدرات — Capability mind map</h1>
<p class="meta" dir="ltr" lang="en">{total} powers · generated by <code>python3 scripts/powers.py mindmap --html</code> · badges: ✅ proven · 🟢 ready · 📦 install · 🔑 key · 👁 seen · 📄 documented · 💡 idea</p>
<div id="diagram" class="card" dir="{'ltr' if getattr(a, 'en', False) else 'rtl'}"><pre class="mermaid">{html.escape(src)}</pre></div>
<p class="tools"><button type="button" id="zoom">Actual size / حجم حقيقي</button></p>
<p id="note">Rendering with Mermaid…</p>
<details id="fallback" open>
<summary>Text view — عرض نصي</summary>
<ul>{''.join(items)}</ul>
</details>
</main>
<script src="{MERMAID_CDN}"></script>
<script>
(function () {{
  var note = document.getElementById('note'), fb = document.getElementById('fallback'), box = document.getElementById('diagram');
  document.getElementById('zoom').addEventListener('click', function () {{ box.classList.toggle('actual'); }});
  function fail(msg) {{ note.textContent = msg; fb.open = true; box.style.display = 'none'; }}
  if (!window.mermaid) {{ fail('Mermaid could not load (offline?) — the text view below has the same map.'); return; }}
  var dark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  try {{
    mermaid.initialize({{ startOnLoad: false, theme: dark ? 'dark' : 'default', securityLevel: 'strict' }});
    mermaid.run({{ querySelector: '.mermaid' }}).then(function () {{ note.textContent = ''; fb.open = false; }})
      .catch(function (e) {{ fail('Mermaid could not draw the map: ' + e); }});
  }} catch (e) {{ fail('Mermaid could not draw the map: ' + e); }}
}})();
</script>
</body>
</html>
"""


def cmd_mindmap(powers, _styles, a) -> int:
    if getattr(a, "domain", None) and not check_domain(powers, a):
        return 2
    src = mindmap_source(powers, a)
    if a.html:
        out = Path(a.html)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(mindmap_html(src, powers, a), encoding="utf-8")
        print(f"wrote {out} ({out.stat().st_size} bytes) — open it in a browser; it falls back to a text list offline")
        return 0
    print(src, end="")
    return 0


def cmd_env(argv: list) -> int:
    sys.path.insert(0, str(HERE))
    try:
        import probe_env
    except ImportError as e:
        print(f"probe_env.py not found next to powers.py: {e}", file=sys.stderr)
        return 1
    return probe_env.main(argv)


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == "env":  # pass every flag straight to probe_env.py
        return cmd_env(argv[1:])
    ap = argparse.ArgumentParser(description="KOSIF Superpowers catalog search / بحث في قدراتك")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("stats"); p.add_argument("--domain"); p.add_argument("--json", action="store_true")
    p = sub.add_parser("search"); p.add_argument("words", nargs="+"); p.add_argument("--limit", type=int, default=25); p.add_argument("--status", nargs="+", choices=STATUSES)
    p.add_argument("--domain"); p.add_argument("--json", action="store_true")
    p = sub.add_parser("show"); p.add_argument("id"); p.add_argument("--json", action="store_true")
    p = sub.add_parser("family"); p.add_argument("family"); p.add_argument("--status", nargs="+", choices=STATUSES); p.add_argument("--json", action="store_true")
    p = sub.add_parser("suggest"); p.add_argument("brief", nargs="+"); p.add_argument("--limit", type=int, default=18)
    p.add_argument("--domain"); p.add_argument("--json", action="store_true")
    p = sub.add_parser("styles"); p.add_argument("--genre", default=""); p.add_argument("--limit", type=int, default=300)
    p = sub.add_parser("domains"); p.add_argument("--json", action="store_true")
    p = sub.add_parser("mindmap"); p.add_argument("--html", metavar="PATH", help="write a standalone HTML page that renders the map")
    p.add_argument("--domain", help="drill into one domain: families → top powers"); p.add_argument("--top", type=int, default=5)
    p.add_argument("--en", action="store_true", help="English labels")
    sub.add_parser("env", help="probe this machine (all flags go to probe_env.py: --json --no-network --install-test --write PATH)")
    a = ap.parse_args(argv)
    powers, styles = load_powers(), load_styles()
    return {"stats": cmd_stats, "search": cmd_search, "show": cmd_show, "family": cmd_family, "suggest": cmd_suggest,
            "styles": cmd_styles, "domains": cmd_domains, "mindmap": cmd_mindmap}[a.cmd](powers, styles, a)


def _entry() -> int:
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # quiet exit when piped into head
    except (AttributeError, ValueError, ImportError):
        pass
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    try:
        return main()
    except BrokenPipeError:
        try:
            devnull = os.open(os.devnull, os.O_WRONLY)
            os.dup2(devnull, sys.stdout.fileno())
        except OSError:
            pass
        return 1


if __name__ == "__main__":
    sys.exit(_entry())
