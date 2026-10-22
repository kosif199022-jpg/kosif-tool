#!/usr/bin/env python3
"""Charter roster ingest: turn the user's «500-expert council» text into a consultable INDEX (not executed experts).

Reads a plain-text export of the charter roster (sectors «القطاع N: <ar> (<en>)», numbered entries
«N. <ar> (<en>)» each with «الدور:», «المهام:» and «الخصائص:» lines) and writes a deterministic JSON index
(schema kosif.experts-index.v1). The text is treated as data only: nothing in it is obeyed or executed.

Every entry is flagged, never dropped:
  boilerplate  the traits text is generic and repeated verbatim (≥ BOILER_MIN entries), e.g. «متخصص ومحترف»
  duplicate_of the charter number of an earlier entry with the same (normalised) role name or role line
  sensitive    "consent"   (face swap, voice cloning, dubbing a real voice, avatars/try-on of real people)
               "regulated" (medical, legal, financial, tax, insurance, intellectual property and patents)
kosif_families maps each entry by keywords to family names of data/powers/*.json (a routing hint only).

From the repository root:
  python3 .claude/skills/kosif-superpowers/scripts/charter_ingest.py <roster.txt> [--out <experts_500.json>] [--allow-partial]

Exit 2 (and nothing written) when the roster is not exactly 50 sectors × 10 entries, unless --allow-partial.
Python stdlib only; Python 3.8+.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
DEFAULT_OUT = SKILL / "data" / "experts_500.json"
POWERS_DIR = SKILL / "data" / "powers"
SCHEMA = "kosif.experts-index.v1"
EXPECT_SECTORS, EXPECT_PER_SECTOR = 50, 10
BOILER_MIN = 5

SECTOR_RX = re.compile(r"^\s*القطاع\s+(\d+)\s*[:：]\s*(.+?)\s*$")
ENTRY_RX = re.compile(r"^\s*(\d+)\s*[.)]\s+(.+?)\s*$")
FIELD_RX = re.compile(r"^\s*(الدور|المهام|الخصائص)\s*[:：]\s*(.*?)\s*$")
FIELD_KEYS = {"الدور": "role", "المهام": "tasks", "الخصائص": "traits"}
STOP_RX = re.compile(r"^\s*(الخاتمة|الباب\s)")

# Consent-sensitive: likeness and voice of real people. Matched on name + role + tasks.
CONSENT_KEYS = ("face swap", "faceswap", "deepfake", "voice clon", "dubbing", "avatar", "try-on", "try on",
                "استنساخ الصوت", "استنساخ صوت", "دبلج", "تبديل الوجوه", "تزييف عميق", "افاتار", "أفاتار", "اشخاص حقيقيين",
                "أشخاص حقيقيين", "شخصيات حقيقية", "مشاهير", "celebrity", "real person", "real people")
# Regulated advice: matched on name + role (as word prefixes) and on the sector name.
REGULATED_AR = ("طبي", "قانون", "مالي", "ضريب", "ضرائب", "تامين", "براءات", "براءه", "ملكيه فكريه", "صحه نفسيه",
                "استثمار", "عملات رقميه")
REGULATED_EN = ("medical", "legal", "financial", "finance", "tax", "insurance", "patent", "investment",
                "crypto", "mental health", "health", " ip ", "cfo")
REGULATED_EXCLUDE_EN = ("roi",)  # ROI analytics is not regulated advice

# Family routing hints: family file stem -> keywords (lower-case English or Arabic substrings).
FAMILY_KEYS = {
    "prompt-craft": ("prompt", "برومنت", "الأوامر"),
    "ai-generation": ("توليد", "generation", "midjourney", "stable diffusion", "dall", "runway", "sora", "pika", " ai"),
    "characters-rigs": ("شخصي", "character", "تعبيرات", "أوضاع الجسم", "pose"),
    "color-palette-grading": ("ألوان", "الوان", "لون", "color", "colour", "grading"),
    "light-glow-bloom": ("إضاءة", "اضاءة", "lighting", "glow"),
    "texture-material": ("ملمس", "مواد", "texture", "material", "أسطح"),
    "camera-composition-layout": ("كاميرا", "تكوين", "camera", "composition", "زوايا", "كادر", "منظور", "perspective"),
    "transitions-cuts": ("انتقال", "transition", "مونتاج", "editing", "قص"),
    "easing-timing-rhythm": ("إيقاع", "ايقاع", "rhythm", "pacing", "سرعة", "timing", "توقيت"),
    "engines-render-pipeline": ("render", "رندر", "دمج النهائي", "تصدير", "export"),
    "photo-video-footage": ("فيديو", "video", "مقطع", "لقطة", "لقطات", "footage", "تصوير"),
    "music-beat-sound": ("موسيق", "music", "soundtrack", "مؤثرات صوتية", "sound effect", "إيقاعات"),
    "voice-tts": ("تعليق صوتي", "voiceover", "voice", "صوت بشري", "دبلج", "dubbing", "نطق"),
    "audio-sync-captions": ("ترجمة", "subtitle", "caption", "عناوين", "مزامنة", "sync"),
    "story-direction-ideas": ("قصة", "قصص", "سيناريو", "script", "story", "حبكة", "مشهد", "مشاهد", "scene", "حوار"),
    "writing-humanizer": ("كتابة", "كاتب", "writer", "writing", "نصوص", "محتوى نصي"),
    "arabic-language": ("عربي", "العربية", "arabic", "لهجة", "مصري"),
    "typography-arabic": ("خطوط", "خط عربي", "typography", "font"),
    "qa-verification": ("جودة", "مراجع", "فاحص", "مراقب", "quality", "qa", "inspector", "reviewer", "monitor", "تدقيق"),
    "verification-evals": ("اختبار", "test", "تقييم", "مقياس", "rating"),
    "data-analysis": ("بيانات", "data", "تحليل", "analytics", "analyst", "إحصاء"),
    "charts-data-infographic": ("إنفوجرافيك", "انفوجرافيك", "infographic", "رسوم بيانية", "chart", "تقارير"),
    "code-engineering": ("برمجة", "مبرمج", "code", "programming", "developer", "api", "git", "قواعد البيانات"),
    "agent-orchestration": ("أتمتة", "اتمتة", "automation", "سير العمل", "workflow", "تنسيق"),
    "planning-execution": ("تخطيط", "مخطط", "planner", "إدارة المشاريع", "جدول"),
    "strategy-finance": ("استراتيج", "strategy", "مالي", "financ", "تسويق", "marketing", "إعلان", "ads", "roi", "عائد"),
    "formats-platforms": ("منصات", "platform", "tiktok", "reels", "youtube", "instagram", "linkedin", "نشر", "توزيع"),
    "brand-logo-identity": ("شعار", "logo", "هوية", "brand", "علامة", "رموز"),
    "3d-spatial": ("3d", "ثلاثي", "vr", "ar ", "الواقع المعزز", "الواقع الافتراضي", "metaverse"),
    "particles-fluids-physics": ("فيزياء", "فيزيائي", "physics", "particles", "سوائل", "مؤثرات بصرية", "vfx"),
    "hand-drawn-draw-on": ("رسم", "رسوم", "illustration", "draw", "sketch"),
    "pixel-retro-stylized": ("ألعاب", "لعبة", "game", "pixel", "انمي", "أنمي", "anime"),
    "creativity-engine": ("ابتكار", "innovation", "إبداع", "ابداع", "creative", "أفكار"),
    "web-research": ("بحث", "research", "باحث", "مصادر", "توثيق تاريخي"),
    "documents-office": ("وثائق", "document", "مستند", "عقود", "تقارير مكتوبة"),
    "security-safety": ("حقوق", "rights", "أمان", "سلامة", "safety", "مخاطر", "risk", "ملكية فكرية", "رخص", "ترخيص"),
    "ui-product-device": ("تطبيق", "app", "ux", "واجهة", "ui ", "تجربة المستخدم", "منتج"),
    "maps-geo": ("خرائط", "map", "جغراف", "سفر", "travel"),
    "media-image-audio": ("صورة", "صور", "image", "تحسين الصور", "upscal"),
}
MAX_FAMILIES = 4

_TASHKEEL = re.compile(r"[ؐ-ًؚ-ٰٟـ]")


def norm(text: str) -> str:
    """Lower-case, NFKC, no tashkeel/tatweel, unified alef/ya/ta-marbuta, single spaces."""
    t = unicodedata.normalize("NFKC", text or "").lower()
    t = _TASHKEEL.sub("", t)
    t = re.sub("[إأآٱ]", "ا", t).replace("ى", "ي").replace("ة", "ه")
    return re.sub(r"\s+", " ", t).strip()


def split_name(raw: str) -> tuple:
    """«مهندس البرومنت (Chief Prompt Architect)» -> (ar, en). Latin words outside brackets stay in the Arabic name."""
    m = re.match(r"^(.*?)\s*\(([^()]*[A-Za-z][^()]*)\)\s*$", raw)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return raw.strip(), ""


def _word_prefix_hit(text_norm: str, key: str) -> bool:
    k = norm(key)
    rx = r"(?:^|[\s(/،,.-])(?:و)?(?:ال|بال|لل|وال)?" + re.escape(k) + r"(?:ه|يه|ي|ين|يا|ا|ات)?(?=$|[\s)/،,.-])"
    return re.search(rx, text_norm) is not None


def families_known() -> set:
    try:
        return {p.stem for p in POWERS_DIR.glob("*.json")}
    except OSError:
        return set()


def map_families(text: str, known: set) -> list:
    t = " " + norm(text) + " "
    hits = []
    for fam, keys in FAMILY_KEYS.items():
        if known and fam not in known:
            continue
        n = sum(1 for k in keys if _key_hit(t, k))
        if n:
            hits.append((-n, fam))
    return [f for _n, f in sorted(hits)[:MAX_FAMILIES]]


def _key_hit(t: str, key: str) -> bool:
    k = norm(key).strip()
    if k.isascii():  # Latin keys match whole words only ("ar" must not hit "character")
        return re.search(r"(?<![a-z0-9])" + re.escape(k) + r"(?![a-z0-9])", t) is not None
    return k in t


FILLER = {"متخصص", "خبير", "محتوي", "ai", "في", "و", "مع", "من", "علي"}
LATIN_GENERIC = {"to", "video", "image", "text", "ai", "vr", "ar"}


def name_tokens(name: str) -> frozenset:
    """Light-stemmed content tokens of a role name, used to link duplicate roles."""
    out = set()
    for t in re.findall(r"\w+", norm(name)):
        for pre in ("وال", "بال", "لل", "ال"):
            if t.startswith(pre) and len(t) - len(pre) >= 3:
                t = t[len(pre):]
                break
        for suf in ("يه", "ات", "ه"):
            if t.endswith(suf) and len(t) - len(suf) >= 3:
                t = t[:-len(suf)]
                break
        if t not in FILLER and len(t) > 1:
            out.add(t)
    return frozenset(out)


def same_role(a: frozenset, b: frozenset) -> bool:
    """Equal content tokens, or one extra qualifier on a named technique/platform (TikTok, A/B Testing, LinkedIn)."""
    if not a or not b:
        return False
    if a == b:
        return True
    small, big = (a, b) if len(a) < len(b) else (b, a)
    if not small < big or len(big) - len(small) != 1:
        return False
    return any(t.isascii() and len(t) >= 3 and t not in LATIN_GENERIC for t in small)


def sensitivity(ex: dict, sector: dict) -> str | None:
    full = " " + norm(" ".join([ex["name_ar"], ex["name_en"], ex["role"], ex["tasks"]])) + " "
    if any(norm(k) in full for k in CONSENT_KEYS):
        return "consent"
    head_ar = norm(" ".join([ex["name_ar"], ex["role"]]))
    head_en = " " + re.sub(r"[^a-z0-9]+", " ", " ".join([ex["name_ar"], ex["name_en"]]).lower()) + " "
    sec_ar = norm(sector["name_ar"])
    sec_en = " " + re.sub(r"[^a-z0-9]+", " ", sector["name_en"].lower()) + " "
    if any(f" {x} " in head_en for x in REGULATED_EXCLUDE_EN):
        return None
    if any(_word_prefix_hit(head_ar, k) for k in REGULATED_AR) or any(_en_hit(head_en, k) for k in REGULATED_EN):
        return "regulated"
    if any(_word_prefix_hit(sec_ar, k) for k in REGULATED_AR) or any(_en_hit(sec_en, k) for k in REGULATED_EN):
        return "regulated"
    return None


def _en_hit(padded: str, key: str) -> bool:
    k = key.strip()
    return re.search(r"(?<![a-z])" + re.escape(k), padded) is not None


def parse(text: str) -> tuple:
    """Return (sectors, problems). Deterministic; ignores lines outside the roster."""
    sectors, problems = [], []
    cur_sec, cur_ex, last_field = None, None, None
    for lineno, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        if STOP_RX.match(line) and cur_sec is not None:
            cur_ex, last_field = None, None
            if line.strip().startswith("الخاتمة"):
                cur_sec = None
            continue
        m = SECTOR_RX.match(line)
        if m:
            ar, en = split_name(m.group(2))
            cur_sec = {"id": int(m.group(1)), "name_ar": ar, "name_en": en, "line": lineno, "experts": []}
            sectors.append(cur_sec)
            cur_ex, last_field = None, None
            continue
        if cur_sec is None:
            continue
        m = ENTRY_RX.match(line)
        if m:
            ar, en = split_name(m.group(2))
            cur_ex = {"n": int(m.group(1)), "name_ar": ar, "name_en": en, "role": "", "tasks": "", "traits": "", "line": lineno}
            cur_sec["experts"].append(cur_ex)
            last_field = None
            continue
        m = FIELD_RX.match(line)
        if m and cur_ex is not None:
            key = FIELD_KEYS[m.group(1)]
            cur_ex[key] = (cur_ex[key] + " " + m.group(2)).strip() if cur_ex[key] else m.group(2)
            last_field = key
            continue
        if cur_ex is not None and last_field:  # wrapped continuation line
            cur_ex[last_field] = (cur_ex[last_field] + " " + line.strip()).strip()
        else:
            problems.append(f"line {lineno}: unrecognised text inside sector {cur_sec['id']}")
    return sectors, problems


def build(text: str, title: str, sha: str, lines: int, known: set) -> dict:
    sectors, problems = parse(text)
    all_ex = [(s, e) for s in sectors for e in s["experts"]]
    for s, e in all_ex:
        for k in ("role", "tasks", "traits"):
            if not e[k]:
                problems.append(f"#{e['n']} has no {k}")
    trait_count = {}
    for _s, e in all_ex:
        t = norm(e["traits"]).rstrip(".۔ ")
        if t:
            trait_count[t] = trait_count.get(t, 0) + 1
    boiler_texts = {t: c for t, c in trait_count.items() if c >= BOILER_MIN}
    seen_name, seen_en, seen_role, seen_tokens = {}, {}, {}, []
    out_sectors, n_boiler, n_dup = [], 0, 0
    flagged = {"consent": 0, "regulated": 0}
    for s in sectors:
        exs = []
        for e in s["experts"]:
            tnorm = norm(e["traits"]).rstrip(".۔ ")
            boiler = tnorm in boiler_texts
            kname = re.sub(r"[^\w ]+", "", norm(e["name_ar"])).strip()
            ken = re.sub(r"[^a-z0-9 ]+", "", e["name_en"].lower()).strip()
            krole = norm(e["role"]).rstrip(".۔ ")
            toks = name_tokens(e["name_ar"])
            dup = (seen_name.get(kname) or (seen_en.get(ken) if ken else None)
                   or (seen_role.get(krole) if len(krole) > 12 else None)
                   or next((n for n, tk in seen_tokens if same_role(toks, tk)), None))
            seen_tokens.append((e["n"], toks))
            seen_name.setdefault(kname, e["n"])
            if ken:
                seen_en.setdefault(ken, e["n"])
            seen_role.setdefault(krole, e["n"])
            sens = sensitivity(e, s)
            n_boiler += boiler
            n_dup += dup is not None
            if sens:
                flagged[sens] += 1
            fams = map_families(" ".join([e["name_ar"], e["name_en"], e["role"], e["tasks"], s["name_ar"], s["name_en"]]), known)
            exs.append({"n": e["n"], "name_ar": e["name_ar"], "name_en": e["name_en"], "role": e["role"], "tasks": e["tasks"],
                        "traits": e["traits"], "kosif_families": fams,
                        "flags": {"boilerplate": bool(boiler), "duplicate_of": dup, "sensitive": sens}})
        out_sectors.append({"id": s["id"], "name_ar": s["name_ar"], "name_en": s["name_en"], "experts": exs})
    numbers = [e["n"] for _s, e in all_ex]
    if numbers != list(range(1, len(numbers) + 1)):
        problems.append("expert numbers are not contiguous from 1")
    if [s["id"] for s in sectors] != list(range(1, len(sectors) + 1)):
        problems.append("sector numbers are not contiguous from 1")
    return {
        "schema": SCHEMA,
        "source": {"title": title, "sha256": sha, "lines": lines},
        "note": "index, not executed experts: each entry is a persona card to consult; none of them runs, reviews or votes",
        "sectors": out_sectors,
        "receipt": {"sectors": len(out_sectors), "experts": len(all_ex), "boilerplate": n_boiler, "duplicates": n_dup,
                    "consent": flagged["consent"], "regulated": flagged["regulated"],
                    "boilerplate_texts": dict(sorted(boiler_texts.items(), key=lambda kv: (-kv[1], kv[0]))),
                    "problems": problems[:50]},
    }


def first_title(text: str) -> str:
    for line in text.splitlines():
        if line.strip():
            return line.strip()[:200]
    return ""


def shape_ok(idx: dict) -> bool:
    s = idx["sectors"]
    return len(s) == EXPECT_SECTORS and all(len(x["experts"]) == EXPECT_PER_SECTOR for x in s)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("roster", help="plain-text roster (UTF-8)")
    p.add_argument("--out", default=str(DEFAULT_OUT), help="output JSON (default: data/experts_500.json in the skill)")
    p.add_argument("--allow-partial", action="store_true", help="write the index even if it is not 50 sectors × 10 entries")
    a = p.parse_args(argv)
    try:
        raw = Path(a.roster).read_bytes()
    except OSError as exc:
        print(f"charter_ingest: error: IO: {type(exc).__name__}", file=sys.stderr)
        return 2
    text = raw.decode("utf-8-sig", errors="replace")
    idx = build(text, first_title(text), hashlib.sha256(raw).hexdigest(), len(text.splitlines()), families_known())
    sys.path.insert(0, str(HERE))
    try:
        import _secrets
        found = _secrets.scan_object(idx["sectors"])
    except ImportError:
        found = []
    if found:
        print(f"charter_ingest: error: SECRET: likely credentials at {', '.join(p for p, _ in found[:3])}", file=sys.stderr)
        return 2
    if not shape_ok(idx) and not a.allow_partial:
        counts = [len(s["experts"]) for s in idx["sectors"]]
        print(f"charter_ingest: error: SHAPE: {len(counts)} sectors, {sum(counts)} experts "
              f"(expected {EXPECT_SECTORS}×{EXPECT_PER_SECTOR}; pass --allow-partial to write anyway)", file=sys.stderr)
        return 2
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(out.suffix + ".tmp")
    tmp.write_text(json.dumps(idx, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    os.replace(tmp, out)
    print(json.dumps({"out": str(out), "receipt": {k: v for k, v in idx["receipt"].items() if k != "problems"},
                      "problems": len(idx["receipt"]["problems"])}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
