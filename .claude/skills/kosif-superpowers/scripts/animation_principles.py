#!/usr/bin/env python3
"""Animation Principles inside KOSIF Superpowers: Dylan Tarre's 144 skills, vendored and routable.

Upstream: https://github.com/dylantarre/animation-principles (MIT (c) 2024 Dylan Tarre).
Every skill applies Disney's 12 principles of animation to one angle of the work: a domain,
a thinking style, a role, a skill level, an animation type, an emotional outcome, a UI element,
an industry, a tool or framework, a time scale, one principle in depth, or a problem type.
The folders are copied unchanged into vendor/animation-principles/ with a SHA-256 manifest;
this tool builds data/animation_principles.json and lets Claude find and read the right skill
from the Superpowers front door (hub.py find).

Commands (from the skill folder):
  python3 scripts/animation_principles.py sync --src <upstream clone> --commit <sha>  # copy + manifest (maintainer)
  python3 scripts/animation_principles.py build              # data/animation_principles.json from the vendored folders
  python3 scripts/animation_principles.py list [--category 07-by-ui-element]
  python3 scripts/animation_principles.py find "<task in the user's words>" [--json]
  python3 scripts/animation_principles.py show <slug>        # description, path and the full SKILL.md with --full
  python3 scripts/animation_principles.py verify             # every vendored file matches its hash

Stdlib only; the skills are text (methods), nothing here is executed.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import superskills as SS  # noqa: E402  (shared helpers: sha256, frontmatter, norm, stem_words, STOP)

SK = Path(__file__).resolve().parents[1]
VENDOR = SK / "vendor" / "animation-principles"
SKILLS = VENDOR / "skills"
MANIFEST = VENDOR / "KOSIF_INTEGRATION.json"
DATA = SK / "data" / "animation_principles.json"
UPSTREAM = "https://github.com/dylantarre/animation-principles"
COPY = ("skills", "docs", "LICENSE", "README.md", "CHANGELOG.md")

# Category folder -> Arabic title, English title, Arabic search words.
CATEGORIES = {
    "01-by-domain": ("حسب المجال", "By domain", "مجال ويب موبايل العاب افلام موشن جرافيك واجهات"),
    "02-by-thinking-style": ("حسب طريقة التفكير", "By thinking style", "تفكير منهج تحليل ابداع"),
    "03-by-role-persona": ("حسب الدور", "By role", "مصمم موشن مطور مخرج منتج معلم رسام"),
    "04-by-skill-level": ("حسب المستوى", "By skill level", "مبتدئ متوسط محترف خبير"),
    "05-by-animation-type": ("حسب نوع الحركة", "By animation type", "دخول خروج تحميل تمرير هوفر انتقال حركة"),
    "06-by-emotional-outcome": ("حسب الإحساس المطلوب", "By emotional outcome", "احساس مشاعر بهجة ثقة هدوء حماس"),
    "07-by-ui-element": ("حسب عنصر الواجهة", "By UI element", "زرار زر قائمة نافذة كارت اشعار ايقونة فورم"),
    "08-by-industry": ("حسب الصناعة", "By industry", "صناعة شركة تطبيق متجر بنك تعليم صحة"),
    "09-by-tool-framework": ("حسب الأداة", "By tool or framework", "اداة مكتبة css framer gsap lottie after effects"),
    "10-by-time-scale": ("حسب المدة", "By time scale", "مدة توقيت سريع بطيء ميلي ثانية"),
    "11-by-principle-focus": ("مبدأ واحد بعمق", "One principle in depth", "مبدا مبادئ ديزني الاثنا عشر squash stretch anticipation"),
    "12-by-problem-type": ("حسب المشكلة", "By problem type", "مشكلة اصلاح بطء دوخة اتاحة اداء"),
}
# Extra Arabic words for skills people ask for often, so Egyptian Arabic requests land on the right one.
SLUG_AR = {
    "buttons-ctas": "زرار زر زراير ضغط كليك", "hover-interactions": "هوفر ماوس يقف عليه مرور المؤشر",
    "loaders-spinners": "لودر تحميل دوامة سبينر", "loading-states": "تحميل انتظار سكيليتون",
    "modals-dialogs": "نافذه منبثقه بوب اب مودال", "notifications-toasts": "اشعار تنبيه توست",
    "navigation-menus": "قائمه منيو تنقل ناف بار", "forms-inputs": "فورم استماره حقل ادخال",
    "cards-containers": "كارت بطاقه", "carousels-sliders": "سلايدر كاروسيل",
    "scroll-animations": "سكرول تمرير", "entrance-animations": "دخول ظهور", "exit-animations": "خروج اختفاء",
    "transition-sequences": "انتقال انتقالات تسلسل", "motion-sickness": "دوخه دوار حساسيه الحركه",
    "accessibility-issues": "اتاحه ذوي الاحتياجات تقليل الحركه", "performance-optimization": "بطء تقطيع اداء سرعه",
    "logo-animation": "لوجو شعار", "character-animation": "شخصيه كاركتر", "text-typography": "نص كتابه تايبوجرافي",
}
COMMON_AR = "انيميشن حركة مبادئ ديزني موشن تحريك animation motion disney principles"


def iter_files(root: Path):
    for p in sorted(root.rglob("*")):
        if p.is_file() and "__pycache__" not in p.parts:
            yield p


def cmd_sync(a) -> int:
    src = Path(a.src).resolve()
    if not (src / "skills").is_dir() or not (src / "LICENSE").is_file():
        print(f"not an animation-principles checkout: {src}", file=sys.stderr)
        return 2
    keep = {"KOSIF_INTEGRATION.json", "KOSIF_README.md"}
    if VENDOR.exists():
        for p in VENDOR.iterdir():
            if p.name not in keep:
                shutil.rmtree(p) if p.is_dir() else p.unlink()
    VENDOR.mkdir(parents=True, exist_ok=True)
    for name in COPY:
        s = src / name
        (shutil.copytree if s.is_dir() else shutil.copy2)(s, VENDOR / name)
    if (src / "CLAUDE.md").is_file():   # renamed so it is not loaded as this repository's instructions
        shutil.copy2(src / "CLAUDE.md", VENDOR / "UPSTREAM-CLAUDE.md")
    old = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.is_file() else {}
    files = {str(p.relative_to(VENDOR)): SS.sha256(p) for p in iter_files(VENDOR) if p.name not in keep}
    man = {
        "name": "Animation Principles (Dylan Tarre) vendored into KOSIF Superpowers",
        "master_skill": "kosif-superpowers",
        "upstream": UPSTREAM,
        "upstream_commit": a.commit or old.get("upstream_commit", ""),
        "upstream_license": "MIT",
        "upstream_original_copyright": "Copyright (c) 2024 Dylan Tarre",
        "integration_mode": "whole skill folders and docs copied unchanged; upstream CLAUDE.md kept as UPSTREAM-CLAUDE.md; routed by scripts/animation_principles.py and hub.py find",
        "kosif_patches": [],
        "skills_count": sum(1 for _ in SKILLS.rglob("SKILL.md")),
        "files": files,
    }
    MANIFEST.write_text(json.dumps(man, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"synced {man['skills_count']} skills, {len(files)} files")
    return cmd_build(a)


def build_records() -> list:
    recs = []
    for p in sorted(SKILLS.rglob("SKILL.md")):
        cat, slug = p.parent.parent.name, p.parent.name
        fm = SS.frontmatter(p.read_text(encoding="utf-8"))
        c = CATEGORIES.get(cat, (cat, cat, ""))
        recs.append({
            "slug": slug, "name": fm.get("name", slug), "category": cat,
            "category_ar": c[0], "category_en": c[1],
            "description": fm.get("description", ""),
            "path": str(p.parent.relative_to(SK)),
            "doc": str((VENDOR / "docs" / cat / f"{slug}.md").relative_to(SK)),
            "search_ar": (c[2] + " " + SLUG_AR.get(slug, "")).strip(),
        })
    return recs


def cmd_build(a) -> int:
    recs = build_records()
    DATA.write_text(json.dumps({"upstream": UPSTREAM, "license": "MIT (c) 2024 Dylan Tarre",
                                "count": len(recs), "skills": recs}, ensure_ascii=False, indent=1) + "\n",
                    encoding="utf-8")
    print(f"wrote {DATA.relative_to(SK)} ({len(recs)} skills)")
    return 0


def load() -> list:
    return json.loads(DATA.read_text(encoding="utf-8"))["skills"]


def terms(s: str) -> set:
    return {w for w in SS.stem_words(SS.norm(s)).split() if w not in SS.STOP and len(w) > 1}


def find(brief: str, limit: int = 5) -> list:
    q = terms(brief)
    if not q:
        return []
    out = []
    for r in load():
        name = terms(r["slug"].replace("-", " ") + " " + r["name"].replace("-", " "))
        body = terms(r["description"] + " " + r["category_en"])
        ar = terms(r["search_ar"] + " " + r["category_ar"] + " " + COMMON_AR)
        own = terms(SLUG_AR.get(r["slug"], ""))
        score = 3.0 * len(q & name) + 1.0 * len(q & body) + 1.0 * len(q & ar) + 2.0 * len(q & own)
        if r["slug"].startswith("universal-"):
            score -= 0.5          # generic fallbacks rank below a specific match
        if score > 0:
            out.append((score, r))
    out.sort(key=lambda x: (-x[0], x[1]["slug"]))
    return out[:limit]


def cmd_find(a) -> int:
    res = find(a.brief, a.limit)
    if a.json:
        print(json.dumps([dict(r, score=s) for s, r in res], ensure_ascii=False, indent=1))
        return 0
    if not res:
        print("no animation-principles skill matched; try: python3 scripts/animation_principles.py list")
        return 0
    for s, r in res:
        print(f"{s:4.1f}  {r['slug']:<28} [{r['category_ar']} / {r['category_en']}]")
        print(f"      {r['description']}")
        print(f"      read: {r['path']}/SKILL.md")
    return 0


def cmd_list(a) -> int:
    cur = None
    for r in load():
        if a.category and r["category"] != a.category:
            continue
        if r["category"] != cur:
            cur = r["category"]
            print(f"\n{cur} — {r['category_ar']} / {r['category_en']}")
        print(f"  {r['slug']}")
    return 0


def cmd_show(a) -> int:
    hits = [r for r in load() if r["slug"] == a.slug]
    if not hits:
        print(f"unknown slug: {a.slug}", file=sys.stderr)
        return 2
    for r in hits:
        print(json.dumps(r, ensure_ascii=False, indent=1))
        if a.full:
            print((SK / r["path"] / "SKILL.md").read_text(encoding="utf-8"))
    return 0


def cmd_verify(a) -> int:
    man = json.loads(MANIFEST.read_text(encoding="utf-8"))
    bad = [f for f, h in man["files"].items() if not (VENDOR / f).is_file() or SS.sha256(VENDOR / f) != h]
    extra = [str(p.relative_to(VENDOR)) for p in iter_files(VENDOR)
             if p.name not in {"KOSIF_INTEGRATION.json", "KOSIF_README.md"} and str(p.relative_to(VENDOR)) not in man["files"]]
    n = sum(1 for _ in SKILLS.rglob("SKILL.md"))
    ok = not bad and not extra and n == man["skills_count"] and len(build_records()) == len(load())
    print(f"animation-principles: {len(man['files'])} files, {n} skills · "
          f"mismatched {len(bad)} · unlisted {len(extra)} · {'OK' if ok else 'FAIL'}")
    for f in bad[:20] + extra[:20]:
        print("  " + f)
    return 0 if ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("sync"); p.add_argument("--src", required=True); p.add_argument("--commit", default="")
    p.set_defaults(fn=cmd_sync)
    sub.add_parser("build").set_defaults(fn=cmd_build)
    p = sub.add_parser("list"); p.add_argument("--category"); p.set_defaults(fn=cmd_list)
    p = sub.add_parser("find"); p.add_argument("brief"); p.add_argument("--limit", type=int, default=5)
    p.add_argument("--json", action="store_true"); p.set_defaults(fn=cmd_find)
    p = sub.add_parser("show"); p.add_argument("slug"); p.add_argument("--full", action="store_true")
    p.set_defaults(fn=cmd_show)
    sub.add_parser("verify").set_defaults(fn=cmd_verify)
    a = ap.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
