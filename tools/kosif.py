#!/usr/bin/env python3
"""KOSIF TOOL command line — أداة سطر الأوامر لأطلس KOSIF.

Python 3 standard library only.  Works from the repository root or anywhere
else (paths resolve from this file).  Run ``python3 tools/kosif.py`` for the
bilingual help, ``python3 tools/kosif.py <command> -h`` for a command.

Commands / الأوامر:
  list      عرض الاستايلات مع فلاتر          list styles with filters
  search    بحث حر في الفهرس                  free-text search over the catalog
  show      عرض سجل استايل وملفه الإبداعي     print one record, its brief and playbooks
  prompt    توليد طلب جاهز لـ Claude Code     fill templates/claude_request.<lang>.txt
  scaffold  إنشاء مجلد مشروع جاهز للعمل       create a project folder with docs, words and a starter
  validate  فحص سلامة المستودع                run tools/validate.py
  stats     إحصاءات الفهرس                    catalog statistics
"""
from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import shutil
import subprocess
import sys
from collections import Counter
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_ROOT = HERE.parent
REPO_URL = "https://github.com/kosif199022-jpg/kosif-tool"

sys.path.insert(0, str(HERE))
from aspects import PRESETS, resolve as resolve_aspect  # noqa: E402  (any W:H, WxH or platform name)

RESOLUTIONS = {k: f"{w}x{h}" for k, (w, h) in PRESETS.items()}
ORIGINS = ("PromptsMotion", "KOSIF original style")
TYPES = ("Prompt", "Skill", "Style")
STARTERS = ("html-canvas", "remotion", "none")
STARTER_IGNORE = ("node_modules", "out", "outputs", "dist", ".git", ".cache", "*.mp4", "*.webm", "*.mov")

# Phrase tables shared with web/generator.js so the website and the CLI emit
# the same request text.  Keys are what the user types on the command line.
STACKS = {
    "auto": {
        "ar": "اختر الأنسب للمادة (Remotion/React للتحرير القابل للتعديل، HTML Canvas أو SVG للرسوم الخفيفة، Three.js للمشاهد الفراغية الحقيقية)",
        "en": "choose the best fit for the material (Remotion/React for editable sequences, HTML Canvas or SVG for light vector motion, Three.js for true spatial scenes)",
    },
    "remotion": {"ar": "Remotion/React (مشروع starters/remotion في المستودع)", "en": "Remotion/React (starters/remotion in the repository)"},
    "canvas": {
        "ar": "HTML Canvas مع خط زمني حتمي (starters/html-canvas) والرندر عبر tools/render_html.cjs",
        "en": "HTML Canvas with a deterministic timeline (starters/html-canvas) rendered through tools/render_html.cjs",
    },
    "svg": {
        "ar": "SVG + GSAP داخل صفحة HTML والرندر عبر tools/render_html.cjs في وضع virtual time",
        "en": "SVG + GSAP in an HTML page rendered through tools/render_html.cjs in virtual-time mode",
    },
    "three": {"ar": "Three.js لمشهد ثلاثي الأبعاد حقيقي مع كاميرا متحركة", "en": "Three.js for a real 3D scene with a moving camera"},
}
SOURCES = {
    "none": {
        "ar": "لا توجد مادة مرفقة — اكتب سردًا قصيرًا أصليًا وخطة مشاهد موقّتة",
        "en": "no material supplied — write a short original narration and a timestamped scene plan",
    },
    "audio": {
        "ar": "ملف صوت مرفق: {detail} — هو المرجع الزمني الأساسي؛ فرّغه وزامن الحركة مع الكلمات",
        "en": "attached audio file: {detail} — it is the master clock; transcribe it and sync motion to the words",
    },
    "video": {
        "ar": "ملف فيديو مرفق: {detail} — ادرس القطعات والحركة والكلام أولًا وحافظ على المادة المصرّح بها",
        "en": "attached video file: {detail} — study its cuts, movement and speech first and preserve the authorized material",
    },
    "text": {"ar": "نص/سكريبت مرفق: {detail}", "en": "attached text/script: {detail}"},
}
AUDIO = {
    "keep": {"ar": "احفظ الصوت المرفق كما هو دون أي تعديل في توقيته", "en": "keep the provided voice untouched, never alter its timing"},
    "music": {
        "ar": "أضف موسيقى مرخّصة فقط مع خفضها تحت الصوت وتسليم بمستوى -14 LUFS",
        "en": "add licensed music only, ducked under the voice, delivered at -14 LUFS",
    },
    "sfx": {"ar": "مؤثرات صوتية قصيرة فقط على اللحظات المفصلية", "en": "short sound effects only on key accents"},
    "silent": {"ar": "بدون صوت", "en": "silent"},
}
LANGS = {
    "ar": {"ar": "العربية فقط (RTL، خط عربي واضح)", "en": "Arabic only (RTL, a clear Arabic typeface)"},
    "en": {"ar": "الإنجليزية فقط", "en": "English only"},
    "both": {"ar": "العربية والإنجليزية معًا مع ضبط اتجاه كل سطر", "en": "Arabic and English together with correct direction per line"},
}

HELP = """KOSIF TOOL — أطلس استايلات الموشن جرافيك لـ Claude Code
KOSIF TOOL — motion graphics style atlas for Claude Code

الاستخدام / Usage:
  python3 tools/kosif.py list     [--category KEY] [--origin PromptsMotion|KOSIF] [--type Prompt|Skill|Style]
                                  [--sort rank|name|published] [--limit N] [--json]
  python3 tools/kosif.py search   <query...> [--limit N] [--json]
  python3 tools/kosif.py show     <id>
  python3 tools/kosif.py prompt   <id> [--lang ar|en] [--aspect 9:16|16:9|1:1|4:5|21:9|2.35:1|1920x816|reel|cinema…] [--fps 30] [--duration 15]
                                  [--source "audio voice.mp3"] [--stack auto|remotion|canvas|svg|three]
                                  [--brand "..."] [--audio keep|music|sfx|silent] [--content-lang ar|en|both]
                                  [--notes "..."] [--out FILE]
  python3 tools/kosif.py scaffold <id> <dir> [--starter html-canvas|remotion|none] [--force] [+ prompt options]
  python3 tools/kosif.py validate
  python3 tools/kosif.py stats    [--json]

الأوامر / Commands:
  list      عرض الاستايلات في جدول مع فلاتر الفئة والمصدر والنوع.
            Table of styles filtered by category, origin and type.
  search    بحث لا يميّز حالة الأحرف في المعرّف والاسم والمنشئ والكلمات المفتاحية والملخصات والفئات.
            Case-insensitive search over id, names, creator, keywords, summaries and categories.
  show      طباعة سجل STYLE.json ثم BRIEF.md إن وُجد ثم مسارات الدلائل.
            Print the STYLE.json record, the BRIEF.md when present, then the playbook paths.
  prompt    تعبئة templates/claude_request.<lang>.txt بطلب جاهز للصق في Claude Code.
            Fill templates/claude_request.<lang>.txt with a ready-to-paste Claude Code request.
  scaffold  إنشاء مجلد يحوي STYLE.md و PLAN.md و TEST_REPORT.md و words.json و REQUEST.md ونسخة من starter.
            Create a folder with STYLE.md, PLAN.md, TEST_REPORT.md, words.json, REQUEST.md and a starter copy.
  validate  تشغيل tools/validate.py والخروج برمزه.
            Run tools/validate.py and exit with its code.
  stats     أعداد حسب المصدر والنوع والفئة ونسبة العرض وأكثر المنشئين وعدد الملفات الإبداعية.
            Counts by origin, type, category and aspect, top creators and brief coverage.

خيارات عامة / Global options:
  --root DIR   جذر المستودع (الافتراضي: مجلد هذا الملف/..). Repository root (default: this file's parent/..).
               Environment variable KOSIF_ROOT is honoured too.

أمثلة / Examples:
  python3 tools/kosif.py search kinetic arabic
  python3 tools/kosif.py prompt pm-stephanlivera-df17a2 --aspect 9:16 --source "audio voice.mp3" --audio keep
  python3 tools/kosif.py scaffold kinetic-arabic ./my-film --starter html-canvas
"""


class CliError(Exception):
    """A user-facing error: printed to stderr, exit code 1."""


# ---------------------------------------------------------------- catalog ---
class Atlas:
    """Read-only view of catalog/styles.json + catalog/categories.json."""

    def __init__(self, root: Path):
        self.root = Path(root)
        self.catalog_path = self.root / "catalog" / "styles.json"
        self.categories_path = self.root / "catalog" / "categories.json"
        self.records = self._load_records()
        self.by_id = {r["id"]: r for r in self.records}
        self.categories = self._load_categories()
        self.cat_by_key = {c["key"]: c for c in self.categories}
        self.legacy = {}
        for c in self.categories:
            for label in c.get("legacy") or []:
                self.legacy[label.lower()] = c["key"]
            self.legacy[c["key"].lower()] = c["key"]
            self.legacy[(c.get("en") or "").lower()] = c["key"]
            self.legacy[(c.get("ar") or "").lower()] = c["key"]

    def _read_json(self, path: Path):
        if not path.exists():
            raise CliError(f"الملف غير موجود / missing file: {path.relative_to(self.root) if path.is_relative_to(self.root) else path}")
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise CliError(f"تعذّر قراءة {path.name} (ربما يُعاد توليده الآن) / cannot parse {path.name} (maybe being regenerated): {exc}")

    def _load_records(self) -> list[dict]:
        data = self._read_json(self.catalog_path)
        if isinstance(data, dict):
            for key in ("styles", "records", "items"):
                if isinstance(data.get(key), list):
                    data = data[key]
                    break
        if not isinstance(data, list):
            raise CliError("catalog/styles.json must be a JSON list of records / يجب أن يكون قائمة سجلات")
        records = [r for r in data if isinstance(r, dict) and isinstance(r.get("id"), str)]
        return records

    def _load_categories(self) -> list[dict]:
        if not self.categories_path.exists():
            return []
        data = self._read_json(self.categories_path)
        return [c for c in data if isinstance(c, dict) and c.get("key")] if isinstance(data, list) else []

    # -- categories ---------------------------------------------------------
    def category_key(self, value: str) -> str | None:
        """Canonical key for a category key, en/ar label or legacy label."""
        if not isinstance(value, str):
            return None
        return self.legacy.get(value.strip().lower())

    def record_categories(self, rec: dict) -> list[str]:
        keys = []
        for raw in rec.get("category") or []:
            key = self.category_key(raw) or raw
            if key not in keys:
                keys.append(key)
        return keys

    def category_label(self, key: str, lang: str = "en") -> str:
        c = self.cat_by_key.get(key)
        if not c:
            return key
        return c.get(lang) or c.get("en") or key

    def playbooks_for(self, rec: dict) -> list[str]:
        listed = [p for p in (rec.get("playbooks") or []) if isinstance(p, str) and p]
        if listed:
            return list(dict.fromkeys(listed))
        out = []
        for key in self.record_categories(rec):
            c = self.cat_by_key.get(key)
            if c and c.get("playbook") and c["playbook"] not in out:
                out.append(c["playbook"])
        return out

    # -- lookup -------------------------------------------------------------
    def find(self, style_id: str) -> dict:
        rec = self.by_id.get(style_id)
        if rec is None:
            rec = self.by_id.get(style_id.strip().lower())
        if rec is not None:
            return rec
        close = self.suggest(style_id)
        hint = ""
        if close:
            hint = "\n  هل تقصد / Did you mean: " + ", ".join(close)
        raise CliError(f"معرّف غير معروف / unknown style id: {style_id!r}{hint}\n  استخدم / use: python3 tools/kosif.py search <query>")

    def suggest(self, query: str, n: int = 5) -> list[str]:
        q = query.strip().lower()
        ids = list(self.by_id)
        close = difflib.get_close_matches(q, ids, n=n, cutoff=0.5)
        # also allow substring hits (e.g. a creator handle or a word of the name)
        for rec in self.records:
            if len(close) >= n:
                break
            hay = " ".join(filter(None, [rec["id"], rec.get("name"), rec.get("name_ar"), rec.get("creator")])).lower()
            if q and q in hay and rec["id"] not in close:
                close.append(rec["id"])
        return close[:n]

    def brief_path(self, rec: dict) -> Path | None:
        rel = rec.get("brief") if isinstance(rec.get("brief"), str) else f"styles/{rec['id']}/BRIEF.md"
        p = self.root / rel
        return p if p.exists() else None

    def style_json(self, rec: dict) -> dict:
        p = self.root / "styles" / rec["id"] / "STYLE.json"
        if p.exists():
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    return data
            except (OSError, ValueError):
                pass
        return rec

    def has_brief(self, rec: dict) -> bool:
        return self.brief_path(rec) is not None


# ---------------------------------------------------------------- helpers ---
def display_name(rec: dict) -> str:
    name = rec.get("name") or rec["id"]
    name_ar = rec.get("name_ar")
    if name_ar and name_ar != name:
        return f"{name} / {name_ar}"
    return name


def trunc(text: str, width: int) -> str:
    text = str(text if text is not None else "")
    return text if len(text) <= width else text[: width - 1] + "…"


def print_table(rows: list[list[str]], headers: list[str], widths: list[int]) -> None:
    def fmt(cells):
        return "  ".join(trunc(c, w).ljust(w) for c, w in zip(cells, widths)).rstrip()

    print(fmt(headers))
    print(fmt(["-" * w for w in widths]))
    for row in rows:
        print(fmt(row))


def fill_template(template: str, variables: dict) -> str:
    """Replace {name} placeholders; unknown placeholders are left untouched."""
    return re.sub(r"\{(\w+)\}", lambda m: str(variables[m.group(1)]) if m.group(1) in variables else m.group(0), template)


def unfilled(text: str) -> list[str]:
    return sorted(set(re.findall(r"\{([A-Za-z_]\w*)\}", text)))


def parse_source(value: str | None, lang: str) -> str:
    """Turn ``--source "audio voice.mp3"`` into the template sentence."""
    if not value or not value.strip():
        return SOURCES["none"][lang]
    value = value.strip()
    head, _, detail = value.partition(" ")
    kind = head.lower()
    if kind in SOURCES:
        detail = detail.strip() or ("(أرفق الملف)" if lang == "ar" else "(attach the file)")
        return SOURCES[kind][lang].replace("{detail}", detail)
    return value  # free text, used verbatim


def parse_audio(value: str | None, lang: str) -> str:
    if not value or not value.strip():
        return AUDIO["keep"][lang]
    key = value.strip().lower()
    return AUDIO[key][lang] if key in AUDIO else value.strip()


def normalize_origin(value: str | None) -> str | None:
    if not value:
        return None
    v = value.strip().lower()
    if v.startswith("kosif"):
        return ORIGINS[1]
    if v.startswith("prompt") or v == "pm":
        return ORIGINS[0]
    raise CliError(f"مصدر غير معروف / unknown origin {value!r}; use PromptsMotion or KOSIF")


def published_key(rec: dict):
    return rec.get("published") or ""


# --------------------------------------------------------------- commands ---
def cmd_list(atlas: Atlas, args) -> int:
    recs = list(atlas.records)
    if args.category:
        key = atlas.category_key(args.category)
        if key is None:
            known = ", ".join(c["key"] for c in atlas.categories)
            raise CliError(f"فئة غير معروفة / unknown category {args.category!r}. Known: {known}")
        recs = [r for r in recs if key in atlas.record_categories(r)]
    origin = normalize_origin(args.origin)
    if origin:
        recs = [r for r in recs if r.get("origin") == origin]
    if args.type:
        want = args.type.strip().lower()
        recs = [r for r in recs if (r.get("type") or "").lower() == want]
    if args.sort == "name":
        recs.sort(key=lambda r: (r.get("name") or "").lower())
    elif args.sort == "published":
        recs.sort(key=published_key, reverse=True)  # newest first, unknown dates ("") last
    else:  # rank
        recs.sort(key=lambda r: (r.get("rank") is None, r.get("rank") or 0, (r.get("name") or "").lower()))
    if args.limit:
        recs = recs[: args.limit]
    if args.json:
        print(json.dumps(recs, ensure_ascii=False, indent=2))
        return 0
    rows = [[r["id"], display_name(r), ", ".join(atlas.record_categories(r)), r.get("type") or "", "" if r.get("rank") is None else str(r["rank"])] for r in recs]
    print_table(rows, ["id", "name", "categories", "type", "rank"], [32, 44, 30, 7, 5])
    print(f"\n{len(recs)} استايل / styles")
    return 0


def search_haystack(atlas: Atlas, rec: dict) -> str:
    parts = [rec.get("id"), rec.get("name"), rec.get("name_ar"), rec.get("creator"), rec.get("summary_ar"), rec.get("summary_en")]
    parts.extend(rec.get("keywords") or [])
    for key in atlas.record_categories(rec):
        parts.append(key)
        c = atlas.cat_by_key.get(key)
        if c:
            parts.extend([c.get("en"), c.get("ar")])
            parts.extend(c.get("legacy") or [])
    for raw in rec.get("category") or []:
        parts.append(raw)
    return " ".join(str(p) for p in parts if p).lower()


def cmd_search(atlas: Atlas, args) -> int:
    terms = [t.lower() for t in " ".join(args.query).split() if t.strip()]
    if not terms:
        raise CliError("اكتب كلمة بحث / give a search query")
    hits = []
    for rec in atlas.records:
        hay = search_haystack(atlas, rec)
        if all(t in hay for t in terms):
            score = sum(2 if t in (rec.get("id") or "").lower() else 1 for t in terms)
            hits.append((score, rec.get("rank") is None, rec.get("rank") or 0, rec))
    hits.sort(key=lambda h: (-h[0], h[1], h[2]))
    recs = [h[3] for h in hits]
    if args.limit:
        recs = recs[: args.limit]
    if args.json:
        print(json.dumps(recs, ensure_ascii=False, indent=2))
        return 0
    if not recs:
        print(f"لا نتائج / no results for: {' '.join(args.query)}")
        return 0
    rows = [[r["id"], display_name(r), ", ".join(atlas.record_categories(r)), r.get("type") or ""] for r in recs]
    print_table(rows, ["id", "name", "categories", "type"], [32, 48, 30, 7])
    print(f"\n{len(recs)} نتيجة / results")
    return 0


def cmd_show(atlas: Atlas, args) -> int:
    rec = atlas.find(args.id)
    data = atlas.style_json(rec)
    print(f"# {rec['id']} — {display_name(rec)}")
    print(f"# styles/{rec['id']}/STYLE.json")
    print(json.dumps(data, ensure_ascii=False, indent=2))
    brief = atlas.brief_path(rec)
    if brief:
        rel = brief.relative_to(atlas.root).as_posix()
        print(f"\n## BRIEF — {rel}\n")
        print(brief.read_text(encoding="utf-8").rstrip())
    else:
        print("\n## BRIEF — لا يوجد ملف إبداعي لهذا الاستايل / no BRIEF.md for this style")
    print("\n## الدلائل / Playbooks")
    pbs = atlas.playbooks_for(rec)
    if not pbs:
        print("- (لا يوجد دليل فئة / no category playbook)")
    for p in pbs:
        state = "موجود / exists" if (atlas.root / p).exists() else "غير موجود بعد / not written yet"
        print(f"- {p}  ({state})")
    skill = rec.get("skill") or "styles/%s/SKILL.md" % rec["id"]
    print(f"\nSKILL: {skill}")
    return 0


def add_prompt_options(p: argparse.ArgumentParser) -> None:
    p.add_argument("--lang", choices=("ar", "en"), default="ar", help="لغة الطلب / request template language (default ar)")
    p.add_argument("--aspect", type=_aspect_arg, default=None, help="نسبة العرض بأي مقاس / any aspect: W:H (21:9, 2.35:1, 3:4), WxH pixels (1920x816) or a name (reel, square, cinema…); default: reference aspect or 9:16")
    p.add_argument("--fps", type=int, default=30, help="إطار/ثانية / frames per second (default 30)")
    p.add_argument("--duration", type=float, default=None, help="المدة بالثواني / duration in seconds (default: brief/record or 15)")
    p.add_argument("--source", default=None, help='المادة المصدرية / source material: "audio voice.mp3", "video clip.mp4", "text script.md", "none" or free text')
    p.add_argument("--stack", choices=tuple(STACKS), default="auto", help="التقنية / implementation stack (default auto)")
    p.add_argument("--brand", default="", help="الهوية البصرية / brand colors, fonts, logo notes")
    p.add_argument("--audio", default="keep", help="الصوت / keep | music | sfx | silent | free text (default keep)")
    p.add_argument("--content-lang", dest="content_lang", choices=tuple(LANGS), default="ar", help="لغة النص داخل الفيديو / on-screen language (default ar)")
    p.add_argument("--notes", default="", help="ملاحظات إضافية / extra notes")


def _aspect_arg(value: str) -> str:
    try:
        label = resolve_aspect(value)[0]  # validate every spec, pixel sizes included
    except ValueError as e:
        raise argparse.ArgumentTypeError(str(e))
    return label if "x" not in value.lower() and "×" not in value else value.strip().lower().replace("×", "x")


def aspect_resolution(aspect: str) -> str:
    _, w, h = resolve_aspect(aspect)
    return f"{w}x{h}"


def default_aspect(rec: dict) -> str:
    label = rec.get("aspect_label")
    if label in RESOLUTIONS:
        return label
    a = rec.get("aspect") or {}
    if isinstance(a, dict) and a.get("w") and a.get("h"):
        return f"{a['w']}x{a['h']}"  # keep the reference's real frame (e.g. 2.35:1)
    return "9:16"


def default_duration(rec: dict) -> float:
    d = rec.get("duration_s")
    return float(d) if isinstance(d, (int, float)) and d > 0 else 15.0


def fmt_num(value: float) -> str:
    return str(int(value)) if float(value).is_integer() else str(value)


def build_prompt(atlas: Atlas, rec: dict, args) -> str:
    lang = args.lang
    template_path = atlas.root / "templates" / f"claude_request.{lang}.txt"
    if not template_path.exists():
        raise CliError(f"القالب غير موجود / template missing: templates/claude_request.{lang}.txt")
    template = template_path.read_text(encoding="utf-8")
    aspect = args.aspect or default_aspect(rec)
    duration = args.duration if args.duration else default_duration(rec)
    playbooks = atlas.playbooks_for(rec)
    if playbooks:
        pb_text = ("، " if lang == "ar" else ", ").join(playbooks)
    else:
        pb_text = "لا يوجد دليل فئة لهذا الاستايل" if lang == "ar" else "no category playbook for this style"
    brief_line = ""
    if atlas.has_brief(rec):
        brief_line = f" و styles/{rec['id']}/BRIEF.md" if lang == "ar" else f" and styles/{rec['id']}/BRIEF.md"
    brand = (args.brand or "").strip() or (
        "لا توجد هوية محددة — اقترح نظام ألوان وخطوط أصليًا ووثّقه في STYLE.md" if lang == "ar" else "no fixed brand — propose an original color and type system and document it in STYLE.md"
    )
    variables = {
        "repo": REPO_URL,
        "id": rec["id"],
        "name": display_name(rec),
        "page": rec.get("page") or "",
        "brief_line": brief_line,
        "playbooks": pb_text,
        "source": parse_source(args.source, lang),
        "aspect": aspect,
        "resolution": aspect_resolution(aspect),
        "fps": str(args.fps),
        "duration": fmt_num(duration),
        "stack": STACKS[args.stack][lang],
        "lang": LANGS[args.content_lang][lang],
        "brand": brand,
        "audio": parse_audio(args.audio, lang),
        "notes": (args.notes or "").strip() or ("لا شيء" if lang == "ar" else "none"),
    }
    text = fill_template(template, variables).strip() + "\n"
    left = unfilled(text)
    if left:
        print(f"تحذير / warning: unfilled placeholders in template: {', '.join(left)}", file=sys.stderr)
    return text


def cmd_prompt(atlas: Atlas, args) -> int:
    rec = atlas.find(args.id)
    text = build_prompt(atlas, rec, args)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print(f"كُتب الطلب إلى / request written to: {out}")
    else:
        sys.stdout.write(text)
    return 0


def doc_variables(atlas: Atlas, rec: dict, args) -> dict:
    aspect = args.aspect or default_aspect(rec)
    duration = args.duration if args.duration else default_duration(rec)
    fps = args.fps
    cats = [f"{atlas.category_label(k, 'en')} / {atlas.category_label(k, 'ar')} ({k})" for k in atlas.record_categories(rec)]
    pbs = atlas.playbooks_for(rec)
    brief = atlas.brief_path(rec)
    return {
        "style_name": display_name(rec),
        "id": rec["id"],
        "page": rec.get("page") or "—",
        "video": rec.get("video") or "—",
        "creator": rec.get("creator") or "—",
        "origin": rec.get("origin") or "—",
        "type": rec.get("type") or "—",
        "categories": "; ".join(cats) if cats else "—",
        "playbooks": ", ".join(pbs) if pbs else "—",
        "skill": rec.get("skill") or f"styles/{rec['id']}/SKILL.md",
        "brief": brief.relative_to(atlas.root).as_posix() if brief else "—",
        "aspect": aspect,
        "resolution": aspect_resolution(aspect),
        "fps": str(fps),
        "duration": fmt_num(duration),
        "frames": str(int(round(duration * fps))),
        "stack": f"{args.stack} — {STACKS[args.stack]['en']}",
        "date": date.today().isoformat(),
        "repo": REPO_URL,
        "difficulty": str(rec.get("difficulty")) if rec.get("difficulty") is not None else "—",
    }


def cmd_scaffold(atlas: Atlas, args) -> int:
    rec = atlas.find(args.id)
    dest = Path(args.dir).expanduser().resolve()
    if dest.exists() and not dest.is_dir():
        raise CliError(f"المسار ليس مجلدًا / not a directory: {dest}")
    if dest.exists() and any(dest.iterdir()) and not args.force:
        raise CliError(f"المجلد غير فارغ / directory is not empty: {dest}\n  أضف --force للكتابة فوق الملفات / add --force to overwrite files")
    dest.mkdir(parents=True, exist_ok=True)
    tdir = atlas.root / "templates"
    variables = doc_variables(atlas, rec, args)
    written: list[str] = []
    missing_templates: list[str] = []
    for name in ("STYLE.md", "PLAN.md", "TEST_REPORT.md"):
        src = tdir / name
        if not src.exists():
            missing_templates.append(name)
            continue
        text = fill_template(src.read_text(encoding="utf-8"), variables)
        left = unfilled(text)
        if left:
            print(f"تحذير / warning: {name} still has placeholders: {', '.join(left)}", file=sys.stderr)
        (dest / name).write_text(text, encoding="utf-8")
        written.append(name)
    words_src = tdir / "words.example.json"
    if words_src.exists():
        shutil.copyfile(words_src, dest / "words.json")
        written.append("words.json")
    else:
        missing_templates.append("words.example.json")
    prompt_text = build_prompt(atlas, rec, args)
    header = (
        f"# REQUEST.md — {variables['style_name']} (`{rec['id']}`)\n\n"
        "انسخ النص أدناه والصقه في Claude Code بعد مشاركة المستودع.\n"
        "Copy the text below and paste it into Claude Code after sharing the repository.\n\n"
    )
    (dest / "REQUEST.md").write_text(header + prompt_text, encoding="utf-8")
    written.append("REQUEST.md")

    starter_note = ""
    if args.starter and args.starter != "none":
        src = atlas.root / "starters" / args.starter
        target = dest / args.starter
        if src.is_dir():
            shutil.copytree(src, target, ignore=shutil.ignore_patterns(*STARTER_IGNORE), dirs_exist_ok=True)
            written.append(f"{args.starter}/ (نسخة من starters/{args.starter} بدون node_modules / copy without node_modules)")
            if (src / "package.json").exists():
                starter_note = f"  شغّل npm install داخل {target.name}/ قبل البدء / run npm install inside {target.name}/ first\n"
        else:
            available = sorted(p.name for p in (atlas.root / "starters").glob("*") if p.is_dir()) if (atlas.root / "starters").exists() else []
            starter_note = (
                f"  تنبيه / notice: starter 'starters/{args.starter}/' غير موجود في المستودع بعد ولم يُنسخ شيء.\n"
                f"  The starter 'starters/{args.starter}/' does not exist in the repository yet; nothing was copied.\n"
                f"  المتاح الآن / available now: {', '.join(available) if available else 'none'}\n"
            )
    print(f"أُنشئ المشروع في / project created at: {dest}")
    for name in written:
        print(f"  + {name}")
    for name in missing_templates:
        print(f"  - تخطّي {name}: القالب غير موجود في templates/ / skipped, template missing", file=sys.stderr)
    if starter_note:
        sys.stdout.write(starter_note)
    print("الخطوة التالية / next: شارك المستودع مع Claude Code والصق REQUEST.md ثم املأ STYLE.md و PLAN.md قبل الرندر.")
    print("Share the repository with Claude Code, paste REQUEST.md, then fill STYLE.md and PLAN.md before rendering.")
    return 0


def cmd_validate(atlas_root: Path, extra: list[str]) -> int:
    script = HERE / "validate.py"
    if not script.exists():
        raise CliError("tools/validate.py غير موجود / is missing")
    cmd = [sys.executable, str(script), "--root", str(atlas_root)] + [a for a in extra if a != "--"]
    return subprocess.call(cmd)


def cmd_stats(atlas: Atlas, args) -> int:
    recs = atlas.records
    by_origin = Counter(r.get("origin") or "unknown" for r in recs)
    by_type = Counter(r.get("type") or "unknown" for r in recs)
    by_cat: Counter = Counter()
    for r in recs:
        by_cat.update(atlas.record_categories(r))
    by_aspect = Counter(r.get("aspect_label") or "unknown" for r in recs)
    creators = Counter(r.get("creator") or "unknown" for r in recs)
    briefs = sum(1 for r in recs if atlas.has_brief(r))
    brief_field = sum(1 for r in recs if r.get("brief"))
    playbooks = sorted({p for c in atlas.categories for p in [c.get("playbook")] if p})
    playbooks_present = sum(1 for p in playbooks if (atlas.root / p).exists())
    data = {
        "total": len(recs),
        "origin": dict(by_origin),
        "type": dict(by_type),
        "category": dict(by_cat.most_common()),
        "aspect_label": dict(by_aspect.most_common()),
        "top_creators": creators.most_common(args.top),
        "with_brief_files": briefs,
        "with_brief_field": brief_field,
        "playbooks_present": playbooks_present,
        "playbooks_declared": len(playbooks),
    }
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0

    def section(title: str, counter):
        print(f"\n{title}")
        for key, n in counter:
            print(f"  {str(key):<28} {n:>5}")

    print(f"الإجمالي / total styles: {len(recs)}")
    section("حسب المصدر / by origin", by_origin.most_common())
    section("حسب النوع / by type", by_type.most_common())
    section("حسب الفئة / by category", by_cat.most_common())
    section("حسب نسبة العرض / by aspect_label", by_aspect.most_common())
    section(f"أكثر المنشئين / top {args.top} creators", creators.most_common(args.top))
    print(f"\nملفات إبداعية / records with BRIEF.md: {briefs} of {len(recs)} (brief field set: {brief_field})")
    print(f"دلائل الفئات / playbooks present: {playbooks_present} of {len(playbooks)} declared in catalog/categories.json")
    return 0


# ------------------------------------------------------------------- main ---
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="kosif.py", add_help=False, description=HELP, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-h", "--help", action="store_true", help="المساعدة / show this help")
    parser.add_argument("--root", default=os.environ.get("KOSIF_ROOT") or str(DEFAULT_ROOT), help="repository root / جذر المستودع")
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("list", help="عرض الاستايلات / list styles", description="عرض الاستايلات مع فلاتر / list styles with filters")
    p.add_argument("--category", help="مفتاح الفئة أو اسمها / category key or label (e.g. charts)")
    p.add_argument("--origin", help="PromptsMotion | KOSIF")
    p.add_argument("--type", help="Prompt | Skill | Style")
    p.add_argument("--sort", choices=("rank", "name", "published"), default="rank", help="الترتيب / sort order (default rank)")
    p.add_argument("--limit", type=int, default=0, help="أقصى عدد صفوف / max rows (0 = all)")
    p.add_argument("--json", action="store_true", help="إخراج JSON / JSON output")

    p = sub.add_parser("search", help="بحث / search", description="بحث حر لا يميّز حالة الأحرف / case-insensitive free-text search")
    p.add_argument("query", nargs="+", help="كلمات البحث / search words (all must match)")
    p.add_argument("--limit", type=int, default=0, help="أقصى عدد نتائج / max results (0 = all)")
    p.add_argument("--json", action="store_true", help="إخراج JSON / JSON output")

    p = sub.add_parser("show", help="عرض سجل / show one record", description="طباعة STYLE.json ثم BRIEF.md ثم الدلائل / print STYLE.json, BRIEF.md and playbooks")
    p.add_argument("id", help="معرّف الاستايل / style id")

    p = sub.add_parser("prompt", help="توليد طلب / generate a Claude Code request", description="تعبئة templates/claude_request.<lang>.txt / fill the request template")
    p.add_argument("id", help="معرّف الاستايل / style id")
    add_prompt_options(p)
    p.add_argument("--out", default=None, help="كتابة الطلب إلى ملف / write the request to this file")

    p = sub.add_parser("scaffold", help="إنشاء مجلد مشروع / create a project folder", description="إنشاء مجلد مشروع مع المستندات والكلمات والطلب / create STYLE.md, PLAN.md, TEST_REPORT.md, words.json, REQUEST.md and a starter")
    p.add_argument("id", help="معرّف الاستايل / style id")
    p.add_argument("dir", help="مجلد الوجهة / destination directory")
    p.add_argument("--starter", choices=STARTERS, default="none", help="نسخة starter / starter to copy (default none)")
    p.add_argument("--force", action="store_true", help="الكتابة فوق مجلد غير فارغ / overwrite files in a non-empty directory")
    add_prompt_options(p)

    p = sub.add_parser("validate", help="فحص المستودع / run tools/validate.py", description="تشغيل tools/validate.py والخروج برمزه / run the validator and exit with its code")
    p.add_argument("extra", nargs="*", help="خيارات تُمرَّر للفاحص / options passed through to validate.py (e.g. --quiet, --json)")

    p = sub.add_parser("stats", help="إحصاءات / statistics", description="إحصاءات الفهرس / catalog statistics")
    p.add_argument("--top", type=int, default=10, help="عدد المنشئين الأعلى / number of top creators (default 10)")
    p.add_argument("--json", action="store_true", help="إخراج JSON / JSON output")
    return parser


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    parser = build_parser()
    args, unknown = parser.parse_known_args(argv)
    if args.help or not args.command:
        print(HELP)
        return 0 if args.help else 2
    if unknown and args.command != "validate":
        parser.error(f"unrecognized arguments / وسائط غير معروفة: {' '.join(unknown)}")
    root = Path(args.root).expanduser().resolve()
    try:
        if args.command == "validate":
            return cmd_validate(root, list(args.extra or []) + list(unknown))
        atlas = Atlas(root)
        handler = {
            "list": cmd_list,
            "search": cmd_search,
            "show": cmd_show,
            "prompt": cmd_prompt,
            "scaffold": cmd_scaffold,
            "stats": cmd_stats,
        }[args.command]
        return handler(atlas, args)
    except CliError as exc:
        print(f"خطأ / error: {exc}", file=sys.stderr)
        return 1
    except BrokenPipeError:
        return 0


if __name__ == "__main__":
    sys.exit(main())
