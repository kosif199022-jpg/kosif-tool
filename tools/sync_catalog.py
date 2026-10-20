#!/usr/bin/env python3
"""Incremental catalog sync for KOSIF TOOL.

Reads the public PromptsMotion library index, detects new / removed entries,
fetches detail pages for entries that are not cached yet, extracts *factual
metadata only* (title, tags, creator, aspect, publish date, model, effort,
technologies named, prompt length) and merges it into catalog/styles.json and
styles/<id>/STYLE.json.  Third-party prompt text, video, posters and music are
never stored in the repository; only links to the owners' pages are kept.

No record is dropped: entries that left the index are kept with listed=false,
and KOSIF styles outside the built-in BASE list (such as 'dua') are carried over
unchanged. Only ids listed in RETIRED (near the top of this file) are removed.

Usage:
  python3 tools/sync_catalog.py              # online sync (uses .cache/ for pages already fetched)
  python3 tools/sync_catalog.py --offline    # rebuild from the cache only (no network)
  python3 tools/sync_catalog.py --refetch    # ignore cached pages and download everything again
  python3 tools/sync_catalog.py --limit 20   # fetch at most 20 new detail pages this run

After a sync run `python3 tools/build.py` to regenerate SKILL.md files,
STYLE_INDEX.md, catalog/playbooks.json, catalog/meta.json and sitemap.xml.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import html
import json
import re
import sys
import time
import urllib.request
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parent.parent
HOST = "https://www.promptsmotion.com"
UA = {"User-Agent": "KOSIF TOOL public-reference catalog/2.0 (+https://github.com/kosif199022-jpg/kosif-tool)"}
CACHE = ROOT / ".cache" / "promptsmotion"
CATALOG = ROOT / "catalog" / "styles.json"
CATEGORIES = ROOT / "catalog" / "categories.json"

# Technologies named in public descriptions.  Only the *name* is recorded.
TECH = {
    "remotion": "Remotion", "three.js": "Three.js", "threejs": "Three.js", "webgl": "WebGL",
    "canvas": "Canvas", "svg": "SVG", "gsap": "GSAP", "css": "CSS", "react": "React",
    "p5": "p5.js", "framer": "Framer Motion", "lottie": "Lottie", "d3": "D3", "anime.js": "anime.js",
    "shader": "Shaders", "glsl": "GLSL", "tailwind": "Tailwind", "web audio": "Web Audio",
    "tone.js": "Tone.js", "manim": "Manim", "motion canvas": "Motion Canvas", "html": "HTML",
}

# KOSIF base styles: id | Arabic name | canonical categories (comma separated)
BASE = """tech-blueprint|رسومات تقنية|diagrams,hand-drawn
comics-panels|لوحات كوميكس|characters,hand-drawn
whiteboard-cinematic|وايتبورد سينمائي|hand-drawn
handwriting-reveal|كتابة يدوية|hand-drawn,kinetic-type
ecommerce-ad|إعلان متجر|ads,product-ui
logo-reveal|كشف شعار|ads,shapes
documentary-map|خريطة وثائقية|diagrams,photos
audio-wave|موجة صوت|music,shapes
chart-race|سباق رسوم|charts
morph-charts|تحولات بيانات|charts,shapes
liquid-morph|أشكال سائلة|shapes,3d
brutalist|بروتالي|kinetic-type
minimal|مينيمال|kinetic-type,shapes
retrowave|ريترو|ads,3d
neon-tech|نيون تقني|ads,particles
parallax-2d|بارالاكس|photos,3d
cinematic-3d|مشاهد 3D سينمائية|3d
lowpoly-3d|مجسمات Low Poly|3d
pixel-art|بيكسل آرت|characters
anime-action|أنمي أكشن|characters
character-rig|تحريك هيكلي|characters
frame-by-frame|إطار بإطار|hand-drawn,characters
stop-motion|ستوب موشن|characters,photos
cutout-paper|قصاصات ورقية|hand-drawn,characters
claymation|صلصال متحرك|characters,3d
higgsfield-journey|جولة سينمائية|3d,photos
scroll-world|عالم تمرير|3d,product-ui
saas-demo|استعراض SaaS|product-ui
ui-micro|واجهات دقيقة|product-ui
glass-ui|واجهة زجاجية|product-ui,shapes
viral-mixed-media|مونتاج مختلط|ads,photos,kinetic-type
editorial|مونتاج تحريري|kinetic-type,photos
typewriter|آلة كتابة|kinetic-type
subtitle-punch|كلمات متحركة|kinetic-type,music
kinetic-arabic|تايبوغرافي عربي|kinetic-type
product|إعلان إطلاق منتج|ads,product-ui
map-journey|رحلة على الخريطة|diagrams
infographic|إنفوجرافيك|charts,diagrams
fake3d|عمق 2.5D|3d,photos
isometric|عالم أيزومتريك|3d,diagrams
stickman|شخصيات عصوية|characters,hand-drawn
chalkboard|سبورة طباشير|hand-drawn
whiteboard|سبورة بيضاء|hand-drawn
doodle|قصص الدودل|hand-drawn
plotter|قلم البلوتر|hand-drawn,shapes"""
# Ids deliberately removed from the catalog, even when BASE or the index still has
# them. A sync rebuilds BASE and the index entries and carries every other existing
# record over (KOSIF styles added by hand such as 'dua', and unlisted PromptsMotion
# entries), so removing an id from BASE alone does not delete it: name it here.
RETIRED: set[str] = set()
# Base styles whose reference lives in motalim-ai/motion-starter-kit (with a reference clip there)
STARTER_KIT = set("plotter doodle whiteboard chalkboard stickman isometric fake3d infographic map-journey product".split())
KOSIF_ONE = "https://github.com/kosif199022-jpg/kosif-one"

BRIEF_FIELDS = ("name_ar", "summary_ar", "summary_en", "keywords", "difficulty", "duration_s", "stack", "brief")
# Fields written by tools/build.py. They are carried over in place, so a sync with
# nothing new rewrites byte-identical records (and the "changed" count stays honest).
DERIVED_FIELDS = ("skill", "playbooks")


def log(*a):
    print(*a, file=sys.stderr, flush=True)


def fetch(url: str, retries: int = 3, timeout: int = 30) -> bytes:
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"fetch failed for {url}: {last}")


def visible(fragment: str) -> str:
    fragment = re.sub(r"<script.*?</script>|<style.*?</style>", "", fragment, flags=re.S)
    text = html.unescape(re.sub(r"<[^>]+>", " ", fragment))
    return re.sub(r"\s+", " ", text).strip()


def aspect_label(w: int | None, h: int | None) -> str | None:
    if not w or not h:
        return None
    r = w / h
    for label, value in (("16:9", 16 / 9), ("9:16", 9 / 16), ("1:1", 1.0), ("4:5", 0.8), ("4:3", 4 / 3), ("21:9", 21 / 9)):
        if abs(r - value) < 0.04:
            return label
    return "other"


def parse_home(doc: str) -> list[dict]:
    cards = []
    for rank, art in enumerate(re.findall(r"<article>(.*?)</article>", doc, re.S), 1):
        slug = re.search(r'href="/([A-Za-z0-9_-]+-[a-f0-9]{6})"', art)
        if not slug:
            continue
        title = re.search(r'aria-label="Open ([^"]*)"', art)
        poster = re.search(r'poster="([^"]+)"', art)
        aspect = re.search(r"aspect-ratio:([0-9]+) / ([0-9]+)", art)
        creator = re.search(r"@<!-- -->([^<]+)</span>", art)
        typ = re.search(r'leading-\[13px\]">([^<]+)</span>', art)
        cards.append({
            "slug": slug.group(1),
            "title": html.unescape(title.group(1)) if title else slug.group(1),
            "poster": urljoin(HOST, poster.group(1)) if poster else None,
            "aspect": {"w": int(aspect.group(1)), "h": int(aspect.group(2))} if aspect else None,
            "creator": ("@" + creator.group(1).strip()) if creator else "unknown",
            "type": typ.group(1).strip() if typ else "Prompt",
            "rank": rank,
        })
    return cards


def parse_detail(doc: str) -> dict:
    out: dict = {}
    ld = re.search(r'<script type="application/ld\+json">(.*?)</script>', doc, re.S)
    ldj = {}
    if ld:
        try:
            ldj = json.loads(ld.group(1))
        except json.JSONDecodeError:
            ldj = {}
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", doc, re.S)
    out["title"] = visible(h1.group(1)) if h1 else None
    tags = []
    m = re.search(r'</h1><div class="mt-4 flex flex-wrap gap-1">(.*?)</div>', doc, re.S)
    if m:
        tags = [visible(x) for x in re.findall(r"<span[^>]*>(.*?)</span>", m.group(1), re.S)]
    out["tags"] = tags
    x = re.search(r'href="(https://x\.com/[^"]+)"', doc)
    out["creator_url"] = x.group(1) if x else None
    typ = re.search(r"« [^»]* » \((Prompt|Skill)\)", doc)
    out["type"] = typ.group(1) if typ else None
    out["published"] = (ldj.get("uploadDate") or "")[:10] or None
    out["video"] = urljoin(HOST, ldj["contentUrl"]) if ldj.get("contentUrl") else None
    out["poster"] = urljoin(HOST, ldj["thumbnailUrl"]) if ldj.get("thumbnailUrl") else None
    if not out["video"]:
        v = re.search(r'<video[^>]*src="([^"]+)"', doc)
        out["video"] = urljoin(HOST, v.group(1)) if v else None
    # The public description region: analysed in memory only, never stored.
    i = doc.find('<h2 class="text-sm text-muted-foreground">Prompt</h2>')
    if i < 0:
        i = doc.find('<h2 class="text-sm text-muted-foreground">Skill</h2>')
    text = visible(doc[i:]) if i >= 0 else ""
    j = text.find("Générateur de prompt")
    body, tail = (text[:j], text[j:]) if j > 0 else (text, "")
    body = re.sub(r"^(Prompt|Skill)\s+Personnaliser\s+Copier\s*", "", body)
    model = re.search(r"Modèle (.+?) Effort", tail)
    effort = re.search(r"Effort (Max|High|Medium|Low)", tail)
    out["model"] = model.group(1).strip() if model else None
    out["effort"] = effort.group(1) if effort else None
    low = body.lower()
    out["tech"] = sorted({v for k, v in TECH.items() if re.search(r"(?<![a-z])" + re.escape(k) + r"(?![a-z])", low)})
    out["source_prompt_words"] = len(body.split()) if body else None
    return out


def load_categories() -> dict:
    cats = json.loads(CATEGORIES.read_text(encoding="utf-8"))
    legacy = {}
    for c in cats:
        legacy[c["key"]] = c["key"]
        for l in c.get("legacy", []):
            legacy[l] = c["key"]
    return legacy


def canonical_categories(values: list[str], legacy: dict) -> list[str]:
    out = []
    for v in values or []:
        k = legacy.get(v)
        if k and k not in out:
            out.append(k)
    return out


def base_records(existing: dict, legacy: dict) -> list[dict]:
    records = []
    for line in BASE.splitlines():
        ident, name, cats = line.split("|")
        if ident in RETIRED:
            continue
        if ident in STARTER_KIT:
            page = f"https://github.com/motalim-ai/motion-starter-kit/tree/main/styles/{ident}"
            blob = page.replace("/tree/", "/blob/")
            video, poster = blob + "/reference.mp4", blob + "/preview.jpg"
        else:
            page, video, poster = KOSIF_ONE, None, None
        old = existing.get(ident, {})
        rec = {
            "id": ident, "name": name, "name_ar": old.get("name_ar") or name, "origin": "KOSIF original style", "type": "Style",
            "category": cats.split(","), "creator": "KOSIF + attributed sources", "creator_url": None,
            "page": page, "video": video, "poster": poster, "aspect": None, "aspect_label": None, "rank": None,
            "published": None, "model": None, "effort": None, "tech": [], "source_prompt_words": None, "listed": True,
        }
        for f in DERIVED_FIELDS + BRIEF_FIELDS:
            if f in old and f != "name_ar":
                rec[f] = old[f]
        records.append(rec)
    return records


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--offline", action="store_true", help="never touch the network; use .cache only")
    ap.add_argument("--refetch", action="store_true", help="re-download cached detail pages")
    ap.add_argument("--limit", type=int, default=0, help="max new detail pages to fetch this run (0 = all)")
    ap.add_argument("--workers", type=int, default=3)
    args = ap.parse_args()

    legacy = load_categories()
    existing = {}
    if CATALOG.exists():
        existing = {r["id"]: r for r in json.loads(CATALOG.read_text(encoding="utf-8"))}
    CACHE.mkdir(parents=True, exist_ok=True)
    (CACHE / "pages").mkdir(exist_ok=True)

    home_path = CACHE / "home.html"
    if args.offline:
        if not home_path.exists():
            log("offline mode but no cached home page"); return 2
        home = home_path.read_text(encoding="utf-8", errors="replace")
    else:
        try:
            raw = fetch(HOST)
            home_path.write_bytes(raw)
            home = raw.decode("utf-8", errors="replace")
        except Exception as e:  # noqa: BLE001
            if home_path.exists():
                log("network failed, using cached home page:", e)
                home = home_path.read_text(encoding="utf-8", errors="replace")
            else:
                log("cannot fetch library index:", e); return 2
    cards = parse_home(home)
    if len(cards) < 50:
        log(f"only {len(cards)} cards parsed; refusing to sync (site markup may have changed)"); return 3
    log(f"library index: {len(cards)} entries")

    todo = []
    for c in cards:
        p = CACHE / "pages" / f"{c['slug']}.html"
        if args.refetch or not p.exists() or p.stat().st_size < 1000:
            todo.append(c["slug"])
    if args.offline and todo:
        log(f"offline: {len(todo)} entries have no cached page and will keep their existing record")
        todo = []
    if args.limit and len(todo) > args.limit:
        log(f"limiting fetch to {args.limit} of {len(todo)} pending pages")
        todo = todo[: args.limit]

    def grab(slug: str) -> tuple[str, str]:
        try:
            raw = fetch(f"{HOST}/{slug}")
            (CACHE / "pages" / f"{slug}.html").write_bytes(raw)
            return slug, "ok"
        except Exception as e:  # noqa: BLE001
            return slug, f"error: {e}"

    if todo:
        log(f"fetching {len(todo)} detail pages…")
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
            for i, (slug, status) in enumerate(pool.map(grab, todo), 1):
                if status != "ok":
                    log(" ", slug, status)
                if i % 25 == 0:
                    log(f"  {i}/{len(todo)}")

    records: list[dict] = base_records(existing, legacy)
    new_ids, changed = [], 0
    for c in cards:
        ident = "pm-" + c["slug"]
        if ident in RETIRED:
            continue
        old = existing.get(ident, {})
        page_path = CACHE / "pages" / f"{c['slug']}.html"
        detail = parse_detail(page_path.read_text(encoding="utf-8", errors="replace")) if page_path.exists() else {}
        cats = canonical_categories(detail.get("tags") or old.get("category") or [], legacy)
        rec = {
            "id": ident,
            "name": detail.get("title") or c["title"] or old.get("name") or c["slug"],
            "name_ar": old.get("name_ar"),
            "origin": "PromptsMotion",
            "type": detail.get("type") or c["type"] or old.get("type") or "Prompt",
            "category": cats,
            "creator": c["creator"] if c["creator"] != "unknown" else old.get("creator", "unknown"),
            "creator_url": detail.get("creator_url") or old.get("creator_url"),
            "page": f"{HOST}/{c['slug']}",
            "video": detail.get("video") or old.get("video"),
            "poster": detail.get("poster") or c["poster"] or old.get("poster"),
            "aspect": c["aspect"] or old.get("aspect"),
            "aspect_label": aspect_label(*(c["aspect"].values())) if c["aspect"] else old.get("aspect_label"),
            "rank": c["rank"],
            "published": detail.get("published") or old.get("published"),
            "model": detail.get("model") or old.get("model"),
            "effort": detail.get("effort") or old.get("effort"),
            "tech": detail.get("tech") if detail else old.get("tech", []),
            "source_prompt_words": detail.get("source_prompt_words") if detail else old.get("source_prompt_words"),
            "listed": True,
        }
        for f in DERIVED_FIELDS + BRIEF_FIELDS:
            if f in old and f != "name_ar":
                rec[f] = old[f]
        if ident not in existing:
            new_ids.append(ident)
        elif {k: v for k, v in old.items() if k != "listed"} != {k: v for k, v in rec.items() if k != "listed"}:
            changed += 1
        records.append(rec)

    # Every other existing record is kept: PromptsMotion entries that disappeared
    # from the public index are flagged listed=false, and KOSIF styles that are not
    # in BASE (for example a measured kit such as 'dua') are carried over unchanged.
    # Only ids named in RETIRED are ever removed.
    seen = {r["id"] for r in records}
    unlisted, kept = 0, 0
    for ident, old in existing.items():
        if ident in seen or ident in RETIRED:
            continue
        old = dict(old)
        if old.get("origin") == "PromptsMotion":
            old["listed"] = False; unlisted += 1
        else:
            kept += 1
        records.append(old)

    CATALOG.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "catalog" / "prompts_motion.json").write_text(
        json.dumps([r for r in records if r["origin"] == "PromptsMotion"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for r in records:
        d = ROOT / "styles" / r["id"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "STYLE.json").write_text(json.dumps(r, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    log(f"catalog: {len(records)} records ({len(new_ids)} new, {changed} changed, {unlisted} unlisted, {kept} other styles kept)")
    if new_ids:
        log("new:", ", ".join(new_ids))
    log("next: python3 tools/build.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
