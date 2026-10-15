#!/usr/bin/env python3
"""Repository validator for KOSIF TOOL — فاحص سلامة المستودع.

Standard library only.  Prints a numbered report and exits 1 when any check
fails (warnings alone keep exit code 0).

  python3 tools/validate.py                # full report
  python3 tools/validate.py --quiet        # only warnings, failures and the summary
  python3 tools/validate.py --json         # machine-readable report
  python3 tools/validate.py --root DIR     # validate another checkout / a test fixture

Checks (see catalog/SCHEMA.md):
  catalog parses and ids are unique · record fields and enums · categories known
  (legacy labels warn) · aspect_label matches aspect · styles/<id>/SKILL.md and
  STYLE.json exist and STYLE.json equals the catalog record · STYLE_INDEX.md
  mentions every id · prompts_motion.json ⊆ styles · briefs.json keys · playbook
  files exist · no rehosted media binaries · request templates share one
  placeholder set.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parent.parent

ORIGINS = {"PromptsMotion", "KOSIF original style"}
TYPES = {"Prompt", "Skill", "Style"}
SCHEMA_ASPECT_LABELS = {"16:9", "9:16", "1:1", "4:5", "4:3", "21:9", "other"}
BRIEF_KEYS = [
    "id", "title_ar", "summary_ar", "summary_en", "concept_ar", "concept_en", "scenes_en", "scenes_ar",
    "motion_rules_en", "motion_rules_ar", "stack", "duration_s", "aspect", "difficulty", "keywords",
    "facts_from_source", "assumptions_en",
]
MEDIA_EXT = {".mp4", ".webm", ".mov", ".mkv", ".avi", ".webp", ".png", ".jpg", ".jpeg", ".gif", ".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac"}
REHOST_MARKER = "promptsmotion.com/__l5e"
MAX_DETAILS = 25
ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
PLACEHOLDER_RE = re.compile(r"\{(\w+)\}")


# ------------------------------------------------------------------ report ---
class Report:
    def __init__(self) -> None:
        self.items: list[dict] = []

    def add(self, status: str, title: str, details: list[str] | None = None) -> None:
        self.items.append({"status": status, "title": title, "details": list(details or [])})

    def check(self, title: str, failures: list[str], warnings: list[str] | None = None, ok_note: str = "") -> None:
        """FAIL when failures exist, WARN when only warnings, PASS otherwise."""
        warnings = warnings or []
        if failures:
            self.add("FAIL", title, failures + [f"(warning) {w}" for w in warnings])
        elif warnings:
            self.add("WARN", title, warnings)
        else:
            self.add("PASS", title, [ok_note] if ok_note else [])

    @property
    def failed(self) -> int:
        return sum(1 for i in self.items if i["status"] == "FAIL")

    @property
    def warned(self) -> int:
        return sum(1 for i in self.items if i["status"] == "WARN")

    def render(self, quiet: bool = False) -> str:
        lines = []
        for n, item in enumerate(self.items, 1):
            if quiet and item["status"] == "PASS":
                continue
            lines.append(f"{n:2d}. [{item['status']}] {item['title']}")
            details = item["details"]
            for d in details[:MAX_DETAILS]:
                lines.append(f"      - {d}")
            if len(details) > MAX_DETAILS:
                lines.append(f"      - ... and {len(details) - MAX_DETAILS} more")
        passed = len(self.items) - self.failed - self.warned
        lines.append("")
        lines.append(f"الخلاصة / summary: {len(self.items)} checks — {passed} passed, {self.warned} warnings, {self.failed} failed")
        lines.append("النتيجة / result: " + ("FAIL" if self.failed else "OK"))
        return "\n".join(lines)


# ----------------------------------------------------------------- helpers ---
def is_https(value) -> bool:
    return isinstance(value, str) and value.startswith("https://") and len(value) > len("https://")


def read_json(path: Path):
    """Return (data, error)."""
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except FileNotFoundError:
        return None, "missing"
    except (OSError, ValueError) as exc:
        return None, f"cannot parse: {exc}"


NAMED_RATIOS = (("16:9", 16 / 9), ("9:16", 9 / 16), ("1:1", 1.0), ("4:5", 0.8), ("4:3", 4 / 3), ("21:9", 21 / 9))
RATIO_TOLERANCE = 0.04  # absolute difference on w/h, same rule as tools/sync_catalog.py


def ratio_label(w: int, h: int) -> str:
    """Named aspect label for a pixel size (first match within RATIO_TOLERANCE, else 'other')."""
    r = w / h
    for label, value in NAMED_RATIOS:
        if abs(r - value) < RATIO_TOLERANCE:
            return label
    return "other"


def label_ratio(label: str) -> float | None:
    m = re.fullmatch(r"(\d+(?:\.\d+)?):(\d+(?:\.\d+)?)", label.strip())
    if not m:
        return None
    try:
        return float(m.group(1)) / float(m.group(2))
    except ZeroDivisionError:
        return None


def iso_date_ok(value: str) -> bool:
    try:
        date.fromisoformat(value[:10])
        return True
    except ValueError:
        return False


def looks_like_media(path: Path) -> bool:
    """Magic-byte sniff for common containers, independent of extension."""
    try:
        with path.open("rb") as fh:
            head = fh.read(16)
    except OSError:
        return False
    if len(head) < 12:
        return False
    if head[4:8] == b"ftyp":  # mp4 / mov / m4a
        return True
    if head[:4] == b"RIFF" and head[8:12] in (b"WEBP", b"AVI ", b"WAVE"):
        return True
    if head[:8] == b"\x89PNG\r\n\x1a\n" or head[:3] == b"\xff\xd8\xff" or head[:6] in (b"GIF87a", b"GIF89a"):
        return True
    if head[:4] == b"\x1aE\xdf\xa3":  # Matroska / WebM
        return True
    if head[:3] == b"ID3" or head[:4] == b"OggS" or head[:4] == b"fLaC":
        return True
    return False


# ------------------------------------------------------------------ checks ---
def run(root: Path) -> Report:
    rep = Report()
    catalog_dir = root / "catalog"
    styles_dir = root / "styles"

    # 1. catalog parses, ids unique ----------------------------------------
    data, err = read_json(catalog_dir / "styles.json")
    records: list[dict] = []
    if err:
        rep.add("FAIL", "catalog/styles.json parses", [err])
    elif not isinstance(data, list):
        rep.add("FAIL", "catalog/styles.json parses", ["top level must be a JSON list of records"])
    else:
        bad = [f"record #{i} is not an object with a string id" for i, r in enumerate(data) if not (isinstance(r, dict) and isinstance(r.get("id"), str))]
        records = [r for r in data if isinstance(r, dict) and isinstance(r.get("id"), str)]
        ids = Counter(r["id"] for r in records)
        dups = [f"duplicate id {k!r} x{n}" for k, n in ids.items() if n > 1]
        malformed = [f"id {r['id']!r} is not a lowercase slug" for r in records if not ID_RE.match(r["id"])]
        rep.check("catalog/styles.json parses and ids are unique", bad + dups + malformed, ok_note=f"{len(records)} records")
    ids_set = {r["id"] for r in records}
    if not records:
        rep.add("FAIL", "catalog has records", ["no usable records — remaining record checks skipped"])

    # 2. categories.json --------------------------------------------------
    cats, err = read_json(catalog_dir / "categories.json")
    cat_keys: dict[str, dict] = {}
    legacy_map: dict[str, str] = {}
    failures = []
    if err:
        failures.append(f"catalog/categories.json {err}")
        cats = []
    elif not isinstance(cats, list):
        failures.append("catalog/categories.json must be a JSON list")
        cats = []
    for i, c in enumerate(cats):
        if not isinstance(c, dict) or not isinstance(c.get("key"), str):
            failures.append(f"category #{i} lacks a string key")
            continue
        for field in ("en", "ar", "playbook"):
            if not isinstance(c.get(field), str) or not c[field]:
                failures.append(f"category {c['key']!r} lacks {field}")
        if c["key"] in cat_keys:
            failures.append(f"duplicate category key {c['key']!r}")
        cat_keys[c["key"]] = c
        for label in c.get("legacy") or []:
            if isinstance(label, str):
                legacy_map[label] = c["key"]
    rep.check("catalog/categories.json is a valid taxonomy", failures, ok_note=f"{len(cat_keys)} categories")

    # 3. record fields and enums ------------------------------------------
    failures, warnings = [], []
    for r in records:
        rid = r["id"]
        if not isinstance(r.get("name"), str) or not r["name"]:
            failures.append(f"{rid}: name must be a non-empty string")
        if r.get("origin") not in ORIGINS:
            failures.append(f"{rid}: origin {r.get('origin')!r} not in {sorted(ORIGINS)}")
        if r.get("type") not in TYPES:
            failures.append(f"{rid}: type {r.get('type')!r} not in {sorted(TYPES)}")
        if not isinstance(r.get("category"), list) or not all(isinstance(x, str) for x in r.get("category") or []):
            failures.append(f"{rid}: category must be a list of strings")
        if not is_https(r.get("page")):
            failures.append(f"{rid}: page must be an https URL, got {r.get('page')!r}")
        for field in ("video", "poster", "creator_url"):
            v = r.get(field)
            if v is not None and not is_https(v):
                failures.append(f"{rid}: {field} must be null or an https URL, got {v!r}")
        a = r.get("aspect")
        if a is not None and not (isinstance(a, dict) and isinstance(a.get("w"), int) and isinstance(a.get("h"), int) and a["w"] > 0 and a["h"] > 0):
            failures.append(f"{rid}: aspect must be null or {{w:int,h:int}}, got {a!r}")
        label = r.get("aspect_label")
        if label is not None and not isinstance(label, str):
            failures.append(f"{rid}: aspect_label must be null or a string")
        rank = r.get("rank")
        if rank is not None and (not isinstance(rank, int) or isinstance(rank, bool) or rank < 1):
            failures.append(f"{rid}: rank must be null or a positive int")
        pub = r.get("published")
        if pub is not None and not (isinstance(pub, str) and iso_date_ok(pub)):
            failures.append(f"{rid}: published must be null or an ISO date, got {pub!r}")
        for field in ("tech", "stack", "keywords", "playbooks"):
            v = r.get(field)
            if v is not None and not (isinstance(v, list) and all(isinstance(x, str) for x in v)):
                failures.append(f"{rid}: {field} must be a list of strings")
        diff = r.get("difficulty")
        if diff is not None and not (isinstance(diff, int) and not isinstance(diff, bool) and 1 <= diff <= 5):
            failures.append(f"{rid}: difficulty must be null or an int 1-5")
        dur = r.get("duration_s")
        if dur is not None and not (isinstance(dur, (int, float)) and not isinstance(dur, bool) and dur > 0):
            failures.append(f"{rid}: duration_s must be null or a positive number")
        skill = r.get("skill")
        if skill != f"styles/{rid}/SKILL.md":
            failures.append(f"{rid}: skill must be 'styles/{rid}/SKILL.md', got {skill!r}")
        brief = r.get("brief")
        if brief is not None and brief != f"styles/{rid}/BRIEF.md":
            failures.append(f"{rid}: brief must be null or 'styles/{rid}/BRIEF.md', got {brief!r}")
        if not isinstance(r.get("creator"), str) or not r["creator"]:
            warnings.append(f"{rid}: creator is empty")
    rep.check("record fields, origin/type enums and URL fields", failures, warnings)

    # 4. categories known --------------------------------------------------
    failures, warnings = [], []
    for r in records:
        for raw in r.get("category") or []:
            if not isinstance(raw, str):
                continue
            if raw in cat_keys:
                continue
            if raw in legacy_map:
                warnings.append(f"{r['id']}: legacy category label {raw!r} (canonical key: {legacy_map[raw]})")
            else:
                failures.append(f"{r['id']}: unknown category {raw!r}")
    rep.check("every category value is a known key (legacy labels only warn)", failures, warnings)

    # 5. aspect_label vs aspect -------------------------------------------
    failures, warnings = [], []
    for r in records:
        a, label = r.get("aspect"), r.get("aspect_label")
        if not (isinstance(a, dict) and isinstance(a.get("w"), int) and isinstance(a.get("h"), int) and a["w"] > 0 and a["h"] > 0):
            continue
        if not isinstance(label, str):
            continue
        actual = a["w"] / a["h"]
        expected = ratio_label(a["w"], a["h"])
        lr = label_ratio(label)
        if lr is not None:
            if abs(lr - actual) >= RATIO_TOLERANCE:
                failures.append(f"{r['id']}: aspect_label {label!r} does not match aspect {a['w']}x{a['h']} (expected: {expected})")
            elif label not in SCHEMA_ASPECT_LABELS:
                warnings.append(f"{r['id']}: aspect_label {label!r} is outside the SCHEMA.md set {sorted(SCHEMA_ASPECT_LABELS)} but matches the pixels")
        elif label == "other":
            if expected != "other":
                failures.append(f"{r['id']}: aspect_label is 'other' but {a['w']}x{a['h']} is {expected}")
        else:
            failures.append(f"{r['id']}: aspect_label {label!r} is not 'W:H' or 'other'")
    rep.check("aspect_label is consistent with aspect", failures, warnings)

    # 6. styles/<id>/SKILL.md + STYLE.json --------------------------------
    failures = []
    for r in records:
        rid = r["id"]
        d = styles_dir / rid
        if not (d / "SKILL.md").is_file():
            failures.append(f"{rid}: styles/{rid}/SKILL.md missing")
        sj = d / "STYLE.json"
        local, err = read_json(sj)
        if err:
            failures.append(f"{rid}: styles/{rid}/STYLE.json {err}")
            continue
        if not isinstance(local, dict) or local.get("id") != rid:
            failures.append(f"{rid}: styles/{rid}/STYLE.json id is {local.get('id') if isinstance(local, dict) else local!r}")
            continue
        if json.dumps(local, sort_keys=True, ensure_ascii=False) != json.dumps(r, sort_keys=True, ensure_ascii=False):
            diff_keys = sorted(k for k in set(local) | set(r) if local.get(k) != r.get(k))
            failures.append(f"{rid}: STYLE.json differs from the catalog record (fields: {', '.join(diff_keys) or 'ordering/other'})")
    rep.check("styles/<id>/SKILL.md and STYLE.json exist and STYLE.json equals the catalog record", failures)

    # 7. orphan style directories ----------------------------------------
    warnings = []
    if styles_dir.is_dir():
        for d in sorted(styles_dir.iterdir()):
            if d.is_dir() and d.name not in ids_set and not d.name.startswith("."):
                warnings.append(f"styles/{d.name}/ has no catalog record")
    rep.check("no orphan directories under styles/", [], warnings)

    # 8. STYLE_INDEX.md mentions every id --------------------------------
    failures = []
    idx = root / "STYLE_INDEX.md"
    if not idx.is_file():
        failures.append("STYLE_INDEX.md missing")
    else:
        text = idx.read_text(encoding="utf-8")
        for r in records:
            rid = r["id"]
            if f"[{rid}]" not in text and f"styles/{rid}/" not in text:
                failures.append(f"{rid}: not mentioned in STYLE_INDEX.md")
    rep.check("STYLE_INDEX.md mentions every id", failures)

    # 9. prompts_motion.json ⊆ styles ------------------------------------
    failures, warnings = [], []
    pm, err = read_json(catalog_dir / "prompts_motion.json")
    if err == "missing":
        warnings.append("catalog/prompts_motion.json missing")
    elif err:
        failures.append(f"catalog/prompts_motion.json {err}")
    elif not isinstance(pm, list):
        failures.append("catalog/prompts_motion.json must be a JSON list")
    else:
        for i, r in enumerate(pm):
            if not isinstance(r, dict) or not isinstance(r.get("id"), str):
                failures.append(f"prompts_motion #{i} lacks a string id")
            elif r["id"] not in ids_set:
                failures.append(f"prompts_motion id {r['id']!r} is not in styles.json")
            elif r.get("origin") != "PromptsMotion":
                warnings.append(f"prompts_motion id {r['id']!r} has origin {r.get('origin')!r}")
    rep.check("catalog/prompts_motion.json ids are a subset of styles.json", failures, warnings)

    # 10. briefs.json -----------------------------------------------------
    failures, warnings = [], []
    briefs, err = read_json(catalog_dir / "briefs.json")
    if err == "missing":
        note = "catalog/briefs.json not present (optional)"
    elif err:
        failures.append(f"catalog/briefs.json {err}")
        note = ""
    elif not isinstance(briefs, dict):
        failures.append("catalog/briefs.json must be an object keyed by id")
        note = ""
    else:
        note = f"{len(briefs)} briefs"
        for bid, b in briefs.items():
            if bid not in ids_set:
                failures.append(f"briefs.json id {bid!r} is not in styles.json")
            if not isinstance(b, dict):
                failures.append(f"briefs.json[{bid!r}] is not an object")
                continue
            missing = [k for k in BRIEF_KEYS if k not in b]
            if missing:
                failures.append(f"briefs.json[{bid!r}] lacks keys: {', '.join(missing)}")
            if b.get("id") not in (None, bid):
                failures.append(f"briefs.json[{bid!r}] has id {b.get('id')!r}")
    # record.brief ↔ BRIEF.md file consistency
    for r in records:
        rid = r["id"]
        f = styles_dir / rid / "BRIEF.md"
        if r.get("brief") and not f.is_file():
            failures.append(f"{rid}: record.brief points to a missing file")
        elif f.is_file() and not r.get("brief"):
            warnings.append(f"{rid}: styles/{rid}/BRIEF.md exists but record.brief is null")
    rep.check("catalog/briefs.json ids and keys, record.brief paths", failures, warnings, ok_note=note)

    # 11. playbooks exist --------------------------------------------------
    failures, warnings = [], []
    referenced: dict[str, str] = {}
    for c in cat_keys.values():
        referenced.setdefault(c["playbook"], f"categories.json[{c['key']}]")
    pbs, err = read_json(catalog_dir / "playbooks.json")
    if err == "missing":
        warnings.append("catalog/playbooks.json not present (optional)")
    elif err:
        failures.append(f"catalog/playbooks.json {err}")
    elif isinstance(pbs, list):
        for i, p in enumerate(pbs):
            if isinstance(p, dict) and isinstance(p.get("path"), str):
                referenced.setdefault(p["path"], f"playbooks.json[{i}]")
            else:
                failures.append(f"playbooks.json #{i} lacks a string path")
    else:
        failures.append("catalog/playbooks.json must be a JSON list")
    for r in records:
        for p in r.get("playbooks") or []:
            referenced.setdefault(p, f"record {r['id']}")
    for path, src in sorted(referenced.items()):
        if not (root / path).is_file():
            failures.append(f"{path} missing (referenced by {src})")
    rep.check("every referenced playbook file exists", failures, warnings, ok_note=f"{len(referenced)} playbook paths")

    # 12. no rehosted media ----------------------------------------------
    failures = []
    for base in (styles_dir, catalog_dir):
        if not base.is_dir():
            continue
        for f in sorted(base.rglob("*")):
            if not f.is_file():
                continue
            rel = f.relative_to(root).as_posix()
            if f.suffix.lower() in MEDIA_EXT:
                failures.append(f"{rel}: media binary inside the repository (links to {REHOST_MARKER} must stay external)")
            elif looks_like_media(f):
                failures.append(f"{rel}: file content looks like a media binary")
    rep.check("no rehosted media under styles/ or catalog/", failures)

    # 13. request templates share one placeholder set ----------------------
    failures, warnings = [], []
    tdir = root / "templates"
    sets = {}
    for lang in ("ar", "en"):
        p = tdir / f"claude_request.{lang}.txt"
        if not p.is_file():
            failures.append(f"templates/claude_request.{lang}.txt missing")
            continue
        sets[lang] = set(PLACEHOLDER_RE.findall(p.read_text(encoding="utf-8")))
    if len(sets) == 2:
        only_ar = sorted(sets["ar"] - sets["en"])
        only_en = sorted(sets["en"] - sets["ar"])
        if only_ar:
            failures.append(f"only in ar template: {', '.join(only_ar)}")
        if only_en:
            failures.append(f"only in en template: {', '.join(only_en)}")
        readme = tdir / "claude_request.README.md"
        if readme.is_file():
            documented = set(re.findall(r"`\{(\w+)\}`", readme.read_text(encoding="utf-8")))
            undocumented = sorted((sets["ar"] | sets["en"]) - documented)
            unused = sorted(documented - (sets["ar"] | sets["en"]))
            if undocumented:
                warnings.append(f"placeholders not documented in claude_request.README.md: {', '.join(undocumented)}")
            if unused:
                warnings.append(f"documented but unused placeholders: {', '.join(unused)}")
    rep.check("templates/claude_request.ar.txt and .en.txt share one placeholder set", failures, warnings, ok_note=f"{len(sets.get('ar', ()))} placeholders")

    # 14. meta.json totals (informational) -------------------------------
    warnings = []
    meta, err = read_json(catalog_dir / "meta.json")
    if err and err != "missing":
        warnings.append(f"catalog/meta.json {err}")
    elif isinstance(meta, dict) and records and meta.get("total") != len(records):
        warnings.append(f"catalog/meta.json total={meta.get('total')} but styles.json has {len(records)} records")
    rep.check("catalog/meta.json totals match (informational)", [], warnings)

    return rep


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description="KOSIF TOOL repository validator / فاحص سلامة المستودع")
    ap.add_argument("--root", default=str(DEFAULT_ROOT), help="repository root / جذر المستودع")
    ap.add_argument("--quiet", action="store_true", help="hide PASS lines / إخفاء الفحوص الناجحة")
    ap.add_argument("--json", action="store_true", help="JSON report / تقرير JSON")
    args = ap.parse_args(argv)
    root = Path(args.root).expanduser().resolve()
    if not (root / "catalog").is_dir():
        print(f"خطأ / error: {root} has no catalog/ directory", file=sys.stderr)
        return 1
    rep = run(root)
    if args.json:
        print(json.dumps({"root": str(root), "failed": rep.failed, "warned": rep.warned, "checks": rep.items}, ensure_ascii=False, indent=2))
    else:
        print(f"KOSIF TOOL validate — {root}")
        print(rep.render(quiet=args.quiet))
    return 1 if rep.failed else 0


if __name__ == "__main__":
    sys.exit(main())
