#!/usr/bin/env python3
"""KOSIF original Telegram typography knowledge index, privacy-first.

Reads exported Telegram HTML, images (header metadata only) and local font tables.
NO font files, image files, raw chat message text, sender data, URLs or local
paths are copied into the PUBLIC atlas. Private source paths remain in a separate
LOCAL-ONLY index that must never be committed. No archives or fonts executed.

Commands:
  doctor        which commands this machine can run (find needs nothing extra)
  find          search the public index (Arabic spelling-tolerant, one row per family/style)
  scan          index loose fonts, chat themes and image headers of ChatExport* folders
  enrich-zips   add fonts found inside ZIP archives (bounded, in memory, never extracted)
  refresh       re-derive tags, name-based license flags, ideas, counts and limitations
                from a PUBLIC index alone (no private files needed)
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote

SCHEMA = "kosif.telegram-typography-index.v3"
COMPATIBLE = ("kosif.telegram-typography-index.v1", "kosif.telegram-typography-index.v2", SCHEMA)
TAGS = {
    "kufi": ("كوفي", "كوفى", "kufi", "kufic", "kufiic"),
    "naskh": ("نسخ", "naskh", "nask"),
    "ruqah": ("رقعة", "رقعه", "ruqaa", "ruqah", "rukah", "riqa"),
    "diwani": ("ديواني", "ديوانى", "diwani"),
    "thuluth": ("ثلث", "thuluth", "thulth", "tholoth"),
    "maghrebi": ("مغربي", "مغربى", "maghrebi", "maghribi"),
    "nastaliq": ("نستعليق", "nastaliq", "nastaleeq"),
    "geometric": ("هندسي", "هندسى", "geometric", "geometry"),
    "calligraphy": ("خط عربي", "خطوط عربية", "calligraphy", "calligraffiti", "كاليجرافي"),
    "brush": ("فرشاة", "فرشه", "brush", "pen", "قلم"),
    "handwritten": ("يدوي", "يدوى", "handwritten", "handwriting", "hand", "handmade", "handlettering"),
    "display": ("عناوين", "بوستر", "poster", "display", "title", "headline", "typography", "تايبو"),
    "logo": ("شعار", "لوجو", "logo", "brand", "branding", "هوية"),
    "bold": ("عريض", "bold", "black", "heavy", "extrabold", "ultra"),
    "light": ("خفيف", "رفيع", "light", "thin", "hairline"),
    "rounded": ("دائري", "دائرى", "مدور", "rounded", "round"),
    "kids": ("اطفال", "أطفال", "kids", "kid", "children", "child", "cartoon", "كرتون"),
    "decorative": ("زخرف", "زخرفة", "زخرفي", "ornament", "ornamental", "decorative", "pattern"),
    "modern": ("حديث", "مودرن", "modern", "contemporary"),
    "vintage": ("قديم", "تراث", "تراثي", "vintage", "retro", "classic"),
    "arabic": ("عربي", "عربى", "عربية", "arabic", "arab", "خط"),
    "latin": ("latin", "english", "انجليزي", "إنجليزي"),
    "motion": ("موشن", "motion", "animation", "تحريك", "animated"),
    "3d": ("3d", "ثري دي", "ثلاثي الأبعاد", "مجسم"),
    "font_creation": ("fontforge", "glyphs", "fontlab", "fonttools", "تصميم خط", "صناعة الخطوط"),
    "licensing": ("license", "ترخيص", "حقوق استخدام", "ofl", "copyright", "مسموح"),
}
# tags too broad to rank by when the query also names a specific style
GENERIC_TAGS = {"arabic", "latin", "display", "bold", "light", "modern", "licensing"}
# a request word that rarely appears in font names borrows nearby styles (lower weight)
QUERY_EXPAND = {"logo": ("display", "geometric", "kufi", "bold"), "kids": ("rounded",), "3d": ("display", "bold"),
                "motion": ("handwritten", "brush", "calligraphy"), "calligraphy": ("thuluth", "diwani", "ruqah", "naskh"),
                "font_creation": ("display",)}
QUERY_STOP = {"خط", "خطوط", "فونت", "فونتات", "font", "fonts", "typeface", "for", "the", "a", "لل", "ل", "في", "من", "و"}
FONT_EXT = {".ttf", ".otf"}
ZIP_FONT_EXT = {".ttf", ".otf", ".woff", ".woff2"}
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
OPEN_LICENSES = {"OFL-claimed-unverified", "Apache-claimed-unverified", "public-domain-claimed-unverified"}
LICENSE_RANK = {"OFL-claimed-unverified": 0, "Apache-claimed-unverified": 0, "public-domain-claimed-unverified": 0,
                "GPL-claimed-unverified": 1, "unknown-no-license-proof": 2, "restricted-or-custom-review": 3, "uninspected": 4}
RESTRICTED_NAME_RX = re.compile(r"(?i)\b(trial|demo|personal[\s_-]*use|unlicen[cs]ed|not[\s_-]*licen[cs]ed|no[\s_-]*licen[cs]e|not[\s_-]*for[\s_-]*commercial|non[\s_-]*commercial)\b")
PERSONAL_AND_COMMERCIAL_RX = re.compile(r"(?i)personal[\s_-]*(?:and|&|/)[\s_-]*commercial")


def restricted_words(text: str) -> bool:
    """Trial/demo/personal-use/unlicensed/non-commercial wording ('personal and commercial use' is not a restriction)."""
    return bool(RESTRICTED_NAME_RX.search(text or "")) and not PERSONAL_AND_COMMERCIAL_RX.search(text or "")
ARABIC_SAMPLE = "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"
LATIN_SAMPLE = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
MAX_MEMBER = 15_000_000          # bytes, per ZIP font member
MAX_RATIO = 120                  # declared uncompressed/compressed ratio
MAX_ENTRIES = 2500               # members per archive
MAX_ARCHIVE = 2_000_000_000      # bytes, per ZIP file
AR_LETTERS = "ء-ي"
IDEA_PATTERNS = [
    ("kufi-grid", "شبكة كوفية هندسية", "kufi", "Square modular strokes, alternate positive/negative space, square Arabic proportions"),
    ("naskh-editorial", "نسخ للتحرير", "naskh", "Balance readability, joining consistency, diacritics and headline-to-body pairing"),
    ("ruqah-personal", "رقعة شخصية", "ruqah", "Casual energetic handwritten joins for invitations and informal visual identity"),
    ("diwani-ceremony", "ديواني فاخر", "diwani", "Ornamental high-contrast lettering for certificates, packaging and luxury"),
    ("thuluth-poster", "ثلث للبوسترات", "thuluth", "Tall sweeping ascenders and decorative hierarchy in heritage compositions"),
    ("arabic-latin-pair", "تزاوج عربي لاتيني", "pair", "Match x-height perception, baseline rhythm and stroke contrast across scripts"),
    ("geometric-logo", "شعار هندسي", "geometric", "Custom minimal letter construction, carefully kerning Arabic and Latin"),
    ("bold-sale", "خط دعائي عريض", "bold", "High-legibility price numerals and weight contrast for promotional posters"),
    ("calligraphy-motion", "الخط المتحرك", "motion", "Reveal letter shapes by stroke order, preserve connection and RTL timing"),
    ("decorative-ornament", "زخرفة حروف", "decorative", "Build repeatable ornaments from legal original outlines, not third-party font tracing"),
    ("brush-doodle", "قلم حر وفرشاة", "brush", "Ink textures and monoline sketch overlay with original strokes"),
    ("3d-glyph", "حروف مجسمة", "3d", "Extrusion, bevel and physically based shadows using independently authorized glyphs"),
    ("display-editorial", "عناوين تحريرية", "display", "Pair strong display Arabic headlines with accessible readable body type"),
    ("light-product", "خط رفيع للمنتجات", "light", "Delicate labels with adequate small-size readability and WCAG contrast"),
    ("identity-system", "نظام هوية طباعية", "identity", "Construct a restrained type system with reusable spacing and size scale"),
    ("kids-rounded", "خط أطفال دائري", "kids", "Wide rounded friendly letters, generous counters and strong contrast for young readers"),
]
# extra tags that stand in for an idea when no font name carries its own tag
THEME_OF = {"pair": "latin", "identity": "logo"}   # which message-theme counter an idea reports
IDEA_FALLBACK = {"geometric": ("kufi", "modern"), "3d": ("display", "bold"), "identity": ("logo", "geometric", "modern"), "kids": ("rounded",),
                 "motion": ("handwritten", "brush", "calligraphy"), "diwani": ("calligraphy",), "thuluth": ("calligraphy",),
                 "decorative": ("calligraphy",)}


def sha_file(path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


# ------------------------------------------------------------------ text
def norm(value) -> str:
    """Lowercase, drop tatweel/harakat and fold Arabic letter variants (أإآ→ا, ة→ه, ى→ي)."""
    s = re.sub(r"[ً-ٰٟـ]", "", str(value or "")).lower()
    s = s.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا").replace("ة", "ه").replace("ى", "ي")
    return re.sub(r"\s+", " ", s).strip()


def _needle_rx(needle: str) -> str:
    n = re.escape(norm(needle))
    if re.search(f"[{AR_LETTERS}]", needle):
        # Arabic: optional conjunction/preposition/article prefix and a short suffix, whole word only
        return rf"(?<![{AR_LETTERS}])(?:[وف])?(?:بال|لل|ال|ب|ل|ك)?{n}(?:ه|ات|ين|ون|يه|يات)?(?![{AR_LETTERS}])"
    return rf"(?<![a-z0-9]){n}s?(?![a-z0-9])"


TAG_RX = {k: re.compile("|".join(_needle_rx(w) for w in v)) for k, v in TAGS.items()}


def tag_text(s) -> list:
    """Whole-word tags (Arabic prefix/suffix tolerant): 'Platinum' is not 'latin', 'مخطوطة' is not 'خط'."""
    lowered = norm(s)
    return [key for key, rx in TAG_RX.items() if rx.search(lowered)]


def clean_name(s) -> str:
    """Public-safe name: no control characters, emails, phone numbers, URLs or @handles."""
    if not s:
        return ""
    s = re.sub(r"[\x00-\x1f]", " ", str(s))
    s = re.sub(r"(?i)\b(?:https?://|www\.)\S+", "", s)
    s = re.sub(r"\b\S+@\S+\.\S+\b", "", s)
    s = re.sub(r"(?<![\w])@[A-Za-z_][\w.]{2,}", "", s)
    s = re.sub(r"(?:\+?\d[\d\-() ]{8,}\d)", "", s)
    return re.sub(r"\s+", " ", s).strip(" -_|,")[:95]


def ext_of(name) -> str:
    """A real-looking extension or '(other)', so text after a dot in a file name never reaches the public file."""
    suf = Path(str(name)).suffix.lower()
    return suf if re.fullmatch(r"\.[a-z0-9]{1,8}", suf) else ("" if not suf else "(other)")


# ------------------------------------------------------------------ font tables
def _name_records(font, ident):
    names = font["name"] if "name" in font else None
    if not names:
        return []
    recs = [r for r in names.names if r.nameID == ident]
    # Windows Unicode English first, other Windows, Unicode platform, then legacy Mac records
    order = lambda r: (0 if (r.platformID, r.langID) == (3, 0x409) else 1 if r.platformID == 3 else 2 if r.platformID == 0 else 3)
    return sorted(recs, key=order)


def utf_name(font, ids) -> str:
    for ident in ids:
        for rec in _name_records(font, ident):
            try:
                s = clean_name(rec.toUnicode())
            except Exception:  # noqa: BLE001
                continue
            if s:
                return s
    return ""


def license_from_text(text: str, names: str = "") -> str:
    """Classify embedded license wording. Restrictive wording wins; nothing here is ever permission."""
    t = (text or "").lower()
    if restricted_words(t) or restricted_words(names):
        return "restricted-or-custom-review"
    if "open font license" in t or "scripts.sil.org/ofl" in t or "openfontlicense" in t or re.search(r"\bofl\b", t):
        return "OFL-claimed-unverified"
    if "apache" in t and "license" in t:
        return "Apache-claimed-unverified"
    if "public domain" in t:
        return "public-domain-claimed-unverified"
    if "gnu" in t and ("license" in t or "gpl" in t):
        return "GPL-claimed-unverified"
    if t and ("all rights reserved" in t or "commercial" in t or "permission" in t):
        return "restricted-or-custom-review"
    return "unknown-no-license-proof"


def license_hint(font, names: str = "") -> str:
    # Read every nameID 13/14 record in full (not the first, not truncated). OS/2 fsType allows
    # embedding but NEVER means the font may legally be redistributed.
    parts = []
    for ident in (13, 14):
        for rec in _name_records(font, ident):
            try:
                parts.append(str(rec.toUnicode()))
            except Exception:  # noqa: BLE001
                pass
    return license_from_text(" ".join(parts), names)


def _table_facts(font, record):
    best = font.getBestCmap() or {}
    record["family"] = utf_name(font, [16, 1]) or "Unnamed font"   # never the private file name
    record["style"] = utf_name(font, [17, 2]) or "Unknown"
    record["postscript_name"] = utf_name(font, [6])
    names = " ".join((record["family"], record["style"], record["postscript_name"]))
    record["license_status"] = license_hint(font, names)
    os2 = font["OS/2"] if "OS/2" in font else None
    record["weight_class"] = int(os2.usWeightClass) if os2 else None
    record["embedding_flags"] = int(os2.fsType) if os2 else None
    record["glyphs"] = len(best)
    record["arabic_codepoints"] = sum(0x600 <= x <= 0x6FF for x in best)
    record["arabic_base_letters_supported"] = sum(ord(x) in best for x in ARABIC_SAMPLE)
    record["arabic_presentation_forms"] = sum(0xFB50 <= x <= 0xFDFF or 0xFE70 <= x <= 0xFEFF for x in best)
    record["latin_basic_letters_supported"] = sum(ord(x) in best for x in LATIN_SAMPLE)
    record["has_arabic"] = record["arabic_base_letters_supported"] >= 20   # real letters, not digits/punctuation
    record["has_latin"] = record["latin_basic_letters_supported"] >= 35
    record["variable"] = "fvar" in font
    record["color_glyphs"] = any(k in font for k in ("COLR", "SVG ", "CBDT", "sbix"))
    record["tags"] = sorted(set(tag_text(names)))
    record["parsed"] = True


def _parse_into(record, stream):
    from fontTools.ttLib import TTFont
    try:
        head = stream.read(4)
        stream.seek(0)
        if head == b"ttcf":   # a collection saved under a .ttf/.otf name: index its first face
            record["collection"] = True
        font = TTFont(stream, lazy=False, recalcBBoxes=False, recalcTimestamp=False, fontNumber=0 if head == b"ttcf" else -1)
        try:
            _table_facts(font, record)
        finally:
            font.close()
    except Exception as e:  # noqa: BLE001
        record.update(family="", style="", parsed=False, parse_error=type(e).__name__, license_status="uninspected", tags=[])
    record["redistribution_approved"] = False   # never automatically permitted from metadata
    record["catalog_id"] = "type-" + record["sha256"][:16]
    return record


def font_record(path):
    import fontTools  # noqa: F401  (fail loudly when missing instead of marking every font unparsed)
    path = Path(path)
    data = path.read_bytes()
    import io
    record = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "extension": ext_of(path.name)}
    with io.BytesIO(data) as stream:
        return _parse_into(record, stream)


def font_from_bytes(data, suffix):
    """Parse bounded ZIP font bytes without extracting to the filesystem."""
    import io
    import fontTools  # noqa: F401
    record = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "extension": ext_of("x" + suffix)}
    with io.BytesIO(data) as stream:
        return _parse_into(record, stream)


# ------------------------------------------------------------------ chats
def read_chat(html):
    import importlib.util
    from bs4 import BeautifulSoup
    parser = "lxml" if importlib.util.find_spec("lxml") else "html.parser"   # same result on Telegram's HTML
    soup = BeautifulSoup(Path(html).read_text(encoding="utf-8-sig", errors="replace"), parser)
    count = 0
    themes = Counter()
    links = Counter()
    notes = []
    for m in soup.select(".message"):
        if "service" in m.get("class", []):
            continue
        count += 1
        txt = m.select_one(".text")
        text = txt.get_text(" ", strip=True) if txt else ""
        found = tag_text(text)
        themes.update(found)
        attached = []   # attachment relative paths only; NO Telegram profile URLs
        for a in m.select("a[href]"):
            link = unquote(a.get("href", "")).replace("\\", "/")
            if (link.startswith("files/") or link.startswith("photos/")) and ".." not in Path(link).parts:
                attached.append(link)
                links[ext_of(link)] += 1
        notes.append({"message_seq": count, "tags": found, "attachments": sorted(set(attached))})
    return {"messages": count, "themes": themes, "linked_extensions": links}, notes


# ------------------------------------------------------------------ derived sections
def family_key(f) -> str:
    """Case-insensitive family name; '' for unparsed fonts and punctuation-only names such as '.'."""
    name = (f.get("family") or "").strip().casefold()
    return name if f.get("parsed", True) and re.search(r"\w", name) else ""


def family_count(fonts) -> int:
    return len({family_key(f) for f in fonts} - {""})


def build_ideas(fonts, themes) -> list:
    """Related fonts per idea across the whole index: distinct families, open-claimed and Arabic-rich first."""
    def related(pred):
        rows = [f for f in fonts if f.get("parsed", True) and pred(f)]
        rows.sort(key=lambda f: (LICENSE_RANK.get(f.get("license_status"), 5), -int(f.get("arabic_codepoints") or 0), f.get("family") or "", f["sha256"]))
        out, seen = [], set()
        for f in rows:
            key = (f.get("family") or "").casefold()
            if key in seen:
                continue
            seen.add(key)
            out.append(f["catalog_id"])
            if len(out) == 12:
                break
        return out
    ideas = []
    for key, label, tag, brief in IDEA_PATTERNS:
        if tag == "pair":
            ids = related(lambda f: f.get("has_arabic") and f.get("has_latin"))
            basis = "fonts covering both Arabic and Latin"
        else:
            ids = related(lambda f, t=tag: t in f.get("tags", []))
            basis = f"font names tagged '{tag}'"
            if len(ids) < 3 and tag in IDEA_FALLBACK:
                more = related(lambda f, alts=IDEA_FALLBACK[tag]: any(a in f.get("tags", []) for a in alts))
                ids += [i for i in more if i not in ids][: 12 - len(ids)]
                basis += " + stand-ins tagged " + "/".join(IDEA_FALLBACK[tag])
        ideas.append({"id": key, "title_ar": label, "design_brief_en": brief,
                      "source_theme_message_hits": int(themes.get(THEME_OF.get(tag, tag), 0)), "related_font_ids": ids, "related_basis": basis,
                      "usage": "Design inspiration only; check font license before actual use"})
    return ideas


def build_limitations(public) -> list:
    sc = public.get("scan_scope", {})
    inv = public.get("archive_inventory", {}).get("zip_members_by_extension", {})
    zips = sc.get("zip_archives_scanned")
    out = ["Photo files were header-scanned for dimensions only; no full image semantic analysis"]
    vs = public.get("visual_sample_review") or {}
    if vs.get("sample_size"):
        out[0] += f"; {vs['sample_size']} photos were visually sampled once, privately"
    if zips:
        out.append(f"ZIP font members (.ttf/.otf/.woff/.woff2) of {zips} archives were read in bounded memory and never extracted; "
                   f"{sc.get('zip_archives_unreadable', 0)} unreadable archive(s) and {sc.get('zip_font_entries_not_parsed', 0)} font member(s) were skipped or failed to parse")
        skipped = {k: v for k, v in inv.items() if k in (".eot", ".glyphs", ".ufo", ".vfb", ".sfd")}
        if skipped:
            out.append("Other font formats inside ZIPs were not indexed: " + ", ".join(f"{k} {v}" for k, v in sorted(skipped.items())))
        out.append("Nested archives, RAR/7z archives, PDFs and encrypted members were not inspected")
    else:
        out.append("ZIP/RAR members and encrypted archives were not inspected")
    out += ["HTML message text categorized via deterministic tags; no raw excerpts published",
            "Font name/OS2 embedding permissions are not copyright licenses",
            "License and original creator permissions must be verified before using or redistributing fonts",
            "Font matching based on metadata does not replace rendering a glyph proof sheet"]
    return out


def finalize(public, themes=None) -> dict:
    fonts = public["fonts"]
    fonts.sort(key=lambda x: (x.get("family") or "", x["sha256"]))
    themes = Counter(themes if themes is not None else public.get("topic_hits_from_message_text", {}))
    lic = Counter(f["license_status"] for f in fonts)
    public["font_license_status_counts"] = dict(sorted(lic.items(), key=lambda kv: (-kv[1], kv[0])))
    public["script_coverage"] = {"fonts_with_arabic": sum(bool(f.get("has_arabic")) for f in fonts),
                                 "fonts_with_latin": sum(bool(f.get("has_latin")) for f in fonts),
                                 "unique_font_families": family_count(fonts),
                                 "unique_family_style_pairs": len({((f.get("family") or "").casefold(), (f.get("style") or "").casefold()) for f in fonts if f.get("parsed", True)})}
    public["typography_design_ideas"] = build_ideas(fonts, themes)
    public["limitations"] = build_limitations(public)
    public["privacy"] = ("No verbatim chats, usernames, contact data, images, source paths or font bytes in the public file; "
                         "URLs and @handles embedded in font names are removed")
    public["schema"] = SCHEMA
    return public


# ------------------------------------------------------------------ scan
def _check_outputs(root, outs, inputs=()):
    outs = [Path(p).expanduser().resolve() for p in outs]
    if len(set(outs)) != len(outs) or set(outs) & {Path(p).resolve() for p in inputs}:
        raise ValueError("outputs must be distinct new files")
    for p in outs:
        if root is not None and (p == root or root in p.parents):
            raise ValueError("outputs must be outside Telegram exports")
        if p.exists() or not p.parent.is_dir():
            raise ValueError("output paths must be new files under existing directories")
    return outs


def scan(root, public_out, private_out, *, max_fonts=20000):
    from PIL import Image
    root = Path(root).expanduser().resolve()
    if not root.is_dir():
        raise ValueError("missing export directory")
    public_out, private_out = _check_outputs(root, (public_out, private_out))
    folders = sorted(p for p in root.iterdir() if p.is_dir() and not p.is_symlink() and p.name.startswith("ChatExport"))
    if not folders:
        raise ValueError("no ChatExport folders")
    aggregate, themes, total_attached = Counter(), Counter(), Counter()
    fonts, private_fonts, private_images, group_stats = [], [], [], []
    seen = set()
    total_messages = 0
    for index, folder in enumerate(folders, 1):
        files = sorted((p for p in folder.rglob("*") if p.is_file() and not p.is_symlink()), key=lambda p: p.as_posix().lower())
        messages = 0
        group_themes, attached, exts = Counter(), Counter(), Counter()
        for html in files:
            if html.suffix.lower() == ".html" and html.name.lower().startswith("messages"):
                info, _notes = read_chat(html)
                messages += info["messages"]
                group_themes.update(info["themes"])
                attached.update(info["linked_extensions"])
        for p in files:
            kind = ext_of(p.name)
            exts[kind] += 1
            aggregate[kind] += 1
            if p.suffix.lower() in FONT_EXT:
                record = font_record(p)
                digest = record["sha256"]
                private_fonts.append({"catalog_id": record["catalog_id"], "relative_source": str(p.relative_to(root)),
                                      "sha256": digest, "family": record.get("family")})
                if digest not in seen:
                    if len(fonts) >= max_fonts:
                        raise ValueError("font safety limit reached")
                    fonts.append(record)
                    seen.add(digest)
            elif p.suffix.lower() in IMAGE_EXT:
                width = height = None
                try:
                    with Image.open(p) as img:
                        width, height = img.size
                except Exception:  # noqa: BLE001
                    pass
                private_images.append({"relative_source": str(p.relative_to(root)), "bytes": p.stat().st_size, "width": width, "height": height})
        total_messages += messages
        themes.update(group_themes)
        total_attached.update(attached)
        group_stats.append({"export_no": index, "files": len(files), "messages_parsed": messages, "extensions": dict(exts),
                            "themes": dict(group_themes), "attached_filetypes": dict(attached)})
    public = {
        "schema": SCHEMA,
        "source": "Telegram Desktop exports, local authorized folder",
        "license_policy": "All source fonts withheld; names and name-table license hints DO NOT grant redistribution or usage rights",
        "scan_scope": {"export_folders": len(folders), "files": sum(x["files"] for x in group_stats), "messages_parsed": total_messages,
                       "loose_unique_font_binaries": len(fonts), "unique_font_binaries": len(fonts),
                       "font_files_seen": len(private_fonts), "images_seen": len(private_images),
                       "unparsed_font_binaries": sum(1 for f in fonts if not f.get("parsed")),
                       "images_fully_reviewed": 0, "executable_attachment_files_executed": 0,
                       "archives_unpacked": 0, "font_read_only_parsing": True},
        "file_types": dict(aggregate),
        "topic_hits_from_message_text": dict(themes),
        "message_attachment_types": dict(total_attached),
        "groups": group_stats,
        "fonts": fonts,
    }
    finalize(public, themes)
    private = {"schema": "kosif.telegram-typography-private.v1", "purpose": "Local-only authorized asset locator, NEVER upload to GitHub",
               "root_path": str(root), "fonts": private_fonts, "images": private_images, "groups": group_stats}
    public_out.write_text(json.dumps(public, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    private_out.write_text(json.dumps(private, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return public


# ------------------------------------------------------------------ ZIP enrichment
def _member_unsafe(m) -> bool:
    name = m.filename.replace("\\", "/")
    while name.startswith("./"):
        name = name[2:]
    parts = name.split("/")
    return (m.file_size > MAX_MEMBER or m.file_size < 16 or m.compress_size > MAX_MEMBER
            or m.file_size / max(1, m.compress_size) > MAX_RATIO or any(part in ("..", ".") for part in parts)
            or name.startswith("/") or re.match(r"^[A-Za-z]:", name) is not None or bool(m.flag_bits & 1))


def _read_bounded(source, m) -> bytes:
    """Decompress at most MAX_MEMBER+1 bytes, whatever the archive declares."""
    with source.open(m) as fh:
        data = fh.read(min(m.file_size, MAX_MEMBER) + 1)
    if len(data) != m.file_size or len(data) > MAX_MEMBER:
        raise ValueError("archive member size mismatch")
    return data


def enrich_zip_archives(root, old_public, old_private, new_public, new_private):
    """Bounded index of ZIP members. No archive contents copied to GitHub."""
    import zipfile
    import fontTools  # noqa: F401
    root = Path(root).expanduser().resolve()
    old_public, old_private = Path(old_public).resolve(), Path(old_private).resolve()
    if not all(x.is_file() for x in (old_public, old_private)):
        raise ValueError("base public and private catalogs required")
    new_public, new_private = _check_outputs(root, (new_public, new_private), inputs=(old_public, old_private))
    public = json.loads(old_public.read_text(encoding="utf8"))
    private = json.loads(old_private.read_text(encoding="utf8"))
    if public.get("schema") not in COMPATIBLE:
        raise ValueError("incompatible prior catalog")
    if Path(private["root_path"]).resolve() != root:
        raise ValueError("private locator belongs to another source")
    existing = {f["sha256"] for f in public["fonts"]}
    loose = public["scan_scope"].get("loose_unique_font_binaries", len(public["fonts"]))
    members, excluded = Counter(), Counter()
    archives = bad_archives = duplicates = new_fonts = unparsed = 0
    archive_reports = []
    folders = [p for p in root.iterdir() if p.is_dir() and not p.is_symlink() and p.name.startswith("ChatExport")]
    zips = sorted(p for d in folders for p in d.rglob("*") if p.suffix.lower() == ".zip" and p.is_file() and not p.is_symlink())
    for z in zips:
        archives += 1
        archive_entry_count = f_count = skip_count = 0
        if z.stat().st_size > MAX_ARCHIVE:
            excluded["oversize_archive"] += 1
            archive_reports.append({"archive_id": "zip-" + hashlib.sha256(str(z.stat().st_size).encode()).hexdigest()[:12],
                                    "entries": 0, "font_entries": 0, "skipped_font_entries": 0})
            continue
        try:
            with zipfile.ZipFile(z) as source:
                infos = source.infolist()
                if len(infos) > MAX_ENTRIES:
                    excluded["oversize_archive_entry_count"] += 1
                    continue
                archive_entry_count = len(infos)
                for m in infos:
                    if m.is_dir():
                        continue
                    ext = ext_of(m.filename)
                    members[ext] += 1
                    if ext not in ZIP_FONT_EXT:
                        continue
                    f_count += 1
                    if _member_unsafe(m):
                        excluded["unsafe_or_encrypted_member"] += 1
                        skip_count += 1
                        continue
                    try:
                        record = font_from_bytes(_read_bounded(source, m), ext)
                    except Exception:  # noqa: BLE001
                        excluded["read_failure"] += 1
                        skip_count += 1
                        continue
                    private["fonts"].append({"catalog_id": record["catalog_id"], "archive_relative": str(z.relative_to(root)),
                                             "zip_member": m.filename, "sha256": record["sha256"], "family": record.get("family")})
                    if record["sha256"] in existing:
                        duplicates += 1
                    else:
                        existing.add(record["sha256"])
                        public["fonts"].append(record)
                        new_fonts += 1
                        if not record.get("parsed"):
                            unparsed += 1
        except Exception:  # noqa: BLE001  (BadZipFile, UnicodeDecodeError, NotImplementedError, zlib errors …)
            bad_archives += 1
            excluded["unreadable_zip"] += 1
        archive_reports.append({"archive_id": "zip-" + sha_file(z)[:12], "entries": archive_entry_count,
                                "font_entries": f_count, "skipped_font_entries": skip_count})
    counts = public["scan_scope"]
    counts.update({"zip_archives_scanned": archives, "zip_archives_unreadable": bad_archives,
                   "zip_font_entries_seen": sum(members.get(x, 0) for x in ZIP_FONT_EXT),
                   "zip_font_entries_new_unique": new_fonts, "zip_fonts_duplicate_existing": duplicates,
                   "zip_font_entries_not_parsed": sum(v for k, v in excluded.items() if k != "unreadable_zip") + unparsed,
                   "loose_unique_font_binaries": loose, "unique_font_binaries": len(public["fonts"]),
                   "font_binary_unique_including_zips": len(public["fonts"]), "raw_archives_extracted": 0})
    public["archive_inventory"] = {"zip_members_by_extension": dict(members), "unreadable_zip_count": bad_archives,
                                   "safety_exclusions": dict(excluded), "archive_identifiers": archive_reports,
                                   "does_not_include_rar_fonts": True}
    finalize(public)
    new_public.write_text(json.dumps(public, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    new_private.write_text(json.dumps(private, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"zip_archives_scanned": archives, "unreadable_zip": bad_archives, "font_entries_in_zips": counts["zip_font_entries_seen"],
            "font_added_unique": new_fonts, "duplicates": duplicates, "unique_font_binaries": len(public["fonts"]),
            "failed_to_parse_nested_fonts": unparsed, "excluded": dict(excluded)}


# ------------------------------------------------------------------ refresh (public index only)
def refresh(old_public, new_public) -> dict:
    """Re-derive everything that the public index alone determines. Deterministic; reads no private file."""
    old_public = Path(old_public).resolve()
    (new_public,) = _check_outputs(None, (new_public,), inputs=(old_public,))
    public = json.loads(old_public.read_text(encoding="utf-8"))
    if public.get("schema") not in COMPATIBLE:
        raise ValueError("incompatible prior catalog")
    input_schema = public.get("schema")
    changed = Counter()
    for f in public["fonts"]:
        for k in ("family", "style", "postscript_name"):
            if f.get(k):
                c = clean_name(f[k])
                if c != f[k]:
                    changed[f"cleaned_{k}"] += 1
                    f[k] = c
        if not f.get("parsed"):
            continue
        names = " ".join(str(f.get(k) or "") for k in ("family", "style", "postscript_name"))
        tags = sorted(set(tag_text(names)))
        if tags != f.get("tags"):
            changed["retagged"] += 1
            f["tags"] = tags
        if f.get("license_status") != "restricted-or-custom-review" and restricted_words(names):
            changed["restricted_by_name"] += 1
            f["license_status"] = "restricted-or-custom-review"
        f["redistribution_approved"] = False
    for f in public["fonts"]:
        if f.pop("duplicates_another_source", None) is not None:
            changed["dropped_duplicates_flag"] += 1
    sc = public["scan_scope"]
    if "loose_unique_font_binaries" not in sc:
        sc["loose_unique_font_binaries"] = sc.get("unique_font_binaries")
    sc["unique_font_binaries"] = len(public["fonts"])
    if "images_semantically_reviewed" in sc:
        sc["images_fully_reviewed"] = sc.pop("images_semantically_reviewed")
    vs = public.get("visual_sample_review") or {}
    if vs.get("sample_size"):
        sc["images_visually_sampled"] = vs["sample_size"]
    finalize(public)
    public["refresh"] = {"by": "telegram_typography_atlas.py refresh", "input_schema": input_schema, "changes": dict(sorted(changed.items()))}
    new_public.write_text(json.dumps(public, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"fonts": len(public["fonts"]), "changes": dict(changed), "license": public["font_license_status_counts"],
            "families": public["script_coverage"]["unique_font_families"]}


# ------------------------------------------------------------------ find
def find(catalog, query, limit=15, has_arabic=None, license_filter="any", collapse=True):
    """Rank fonts by style tags and name words. One row per family (its styles listed), open-claimed licenses
    first on ties. Words that rarely occur in font names (logo, kids, 3d …) borrow nearby styles at lower weight."""
    q = norm(query)
    if not q:
        raise ValueError("query required")
    tags = tag_text(q)
    specific = [t for t in tags if t not in GENERIC_TAGS]
    rank_tags = specific or tags
    near = sorted({e for t in rank_tags for e in QUERY_EXPAND.get(t, ())} - set(rank_tags))
    want_variable = bool(re.search(r"(?<![\w])(variable|متغير|متغيره)(?![\w])", q))
    words = [w for w in re.findall(r"[\w]+", q) if w not in QUERY_STOP and len(w) > 1 and not (want_variable and w in ("variable", "متغير", "متغيره"))]
    words = [w for w in words if not any(TAG_RX[t].search(w) for t in tags)] or ([] if rank_tags else words)
    groups = {}
    for font in catalog["fonts"]:
        if has_arabic is not None and bool(font.get("has_arabic")) != has_arabic:
            continue
        if license_filter == "open" and font.get("license_status") not in OPEN_LICENSES:
            continue
        ftags = font.get("tags", [])
        name = norm(f"{font.get('family', '')} {font.get('style', '')}")
        score = sum(5 for t in rank_tags if t in ftags) + sum(2 for t in near if t in ftags) + (5 if want_variable and font.get("variable") else 0)
        if words:
            exact = norm(" ".join(words))
            score += 12 if re.search(rf"(?<![\w]){re.escape(exact)}(?![\w])", name) else sum(
                2 for w in words if re.search(rf"(?<![\w]){re.escape(w)}", name))
        if not score:
            continue
        key = (family_key(font) or font["catalog_id"]) if collapse else font["catalog_id"]
        sort = (-score, LICENSE_RANK.get(font.get("license_status"), 5), -int(font.get("arabic_codepoints") or 0), font.get("family") or "", font["catalog_id"])
        g = groups.setdefault(key, {"sort": sort, "score": score, "font": font, "styles": set(), "copies": 0, "licenses": set()})
        g["styles"].add(font.get("style") or "")
        g["copies"] += 1
        g["licenses"].add(font.get("license_status"))
        if sort < g["sort"]:
            g.update(sort=sort, score=score, font=font)
    rows = sorted(groups.values(), key=lambda g: g["sort"])
    out = []
    for g in rows[:limit]:
        x = g["font"]
        out.append({"font_id": x["catalog_id"], "family": x.get("family"), "style": x.get("style"),
                    "styles": sorted(s for s in g["styles"] if s)[:12], "files": g["copies"],
                    "arabic_glyphs": x.get("arabic_codepoints", 0), "latin": bool(x.get("has_latin")), "variable": bool(x.get("variable")),
                    "weight_class": x.get("weight_class"), "tags": x.get("tags", []), "license_status": x["license_status"],
                    "license_mixed": len(g["licenses"]) > 1, "score": g["score"]})
    return out


# ------------------------------------------------------------------ CLI
def doctor() -> dict:
    import importlib.util as u
    have = {m: u.find_spec(m) is not None for m in ("bs4", "lxml", "fontTools", "PIL", "brotli")}
    return {"ready": {"find": True, "refresh": True, "scan": all(have[m] for m in ("bs4", "fontTools", "PIL")),
                      "enrich-zips": have["fontTools"], "woff2-in-zips": have["fontTools"] and have["brotli"]},
            "modules": have, "install": "pip install beautifulsoup4 fonttools[woff] Pillow  (lxml optional, faster)",
            "reads": ["export HTML", "TTF", "OTF", "WOFF/WOFF2 inside ZIP", "image headers"], "raw_uploads": False}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    subs = ap.add_subparsers(dest="action", required=True)
    subs.add_parser("doctor")
    s = subs.add_parser("scan")
    s.add_argument("--root", required=True)
    s.add_argument("--public-out", required=True)
    s.add_argument("--private-out", required=True)
    s.add_argument("--max-fonts", type=int, default=20000, help="stop (writing nothing) after this many distinct fonts")
    z = subs.add_parser("enrich-zips")
    for option in ("root", "public", "private", "new-public", "new-private"):
        z.add_argument("--" + option, required=True)
    r = subs.add_parser("refresh")
    r.add_argument("--index", required=True)
    r.add_argument("--out", required=True)
    f = subs.add_parser("find")
    f.add_argument("--index", required=True)
    f.add_argument("query")
    f.add_argument("--limit", type=int, default=15)
    f.add_argument("--arabic-only", action="store_true")
    f.add_argument("--license", choices=("any", "open"), default="any", help="open = OFL/Apache/public-domain claims only (still unverified)")
    f.add_argument("--all-copies", action="store_true", help="do not collapse identical family/style rows")
    args = ap.parse_args(argv)
    try:
        if args.action == "doctor":
            print(json.dumps(doctor(), ensure_ascii=False))
        elif args.action == "scan":
            res = scan(args.root, args.public_out, args.private_out, max_fonts=args.max_fonts)
            print(json.dumps({"scan_scope": res["scan_scope"], "licenses": res["font_license_status_counts"],
                              "design_briefs": len(res["typography_design_ideas"])}, ensure_ascii=False))
        elif args.action == "enrich-zips":
            print(json.dumps(enrich_zip_archives(args.root, args.public, args.private, args.new_public, args.new_private), ensure_ascii=False))
        elif args.action == "refresh":
            print(json.dumps(refresh(args.index, args.out), ensure_ascii=False))
        else:
            catalog = json.loads(Path(args.index).read_text(encoding="utf-8"))
            print(json.dumps(find(catalog, args.query, max(1, min(50, args.limit)), True if args.arabic_only else None,
                                  args.license, not args.all_copies), ensure_ascii=False, indent=2))
        return 0
    except Exception as e:  # noqa: BLE001
        print(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
