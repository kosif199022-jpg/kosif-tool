#!/usr/bin/env python3
"""100 Super Skills inside KOSIF Superpowers: the owner's 114-skill repository, vendored and routable.

The owner's repository kosif199022-jpg/100-superskills (MIT) holds 114 Claude skills: 110 catalogued
super skills plus kosif-one, kosif-social, kosif-mimic and kosif-montage-motion. This tool copies them
into vendor/100-superskills/ with a SHA-256 manifest, builds data/superskills.json, and lets Claude
find, read, install and test any of them from the Superpowers front door.

Commands (from the skill folder):
  python3 scripts/superskills.py sync --src ../100-superskills   # copy the skills + write the manifest (owner action)
  python3 scripts/superskills.py build                           # data/superskills.json from the vendored folders
  python3 scripts/superskills.py list [--domain motion]           # all 114, grouped by domain
  python3 scripts/superskills.py find "<task in the user's words>" [--json]
  python3 scripts/superskills.py show <slug>                     # description, path, scripts, tests, sources
  python3 scripts/superskills.py install <slug> [--dest ~/.claude/skills] [--dry-run]
  python3 scripts/superskills.py verify                          # every vendored file matches its hash
  python3 scripts/superskills.py selftest [<slug> ...]           # run the skills' own unit tests in a temp copy

Stdlib only. It never runs a vendored script except the skill's own tests under `selftest`,
and those run in a temporary copy so the vendor folder stays clean.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
VENDOR = SK / "vendor" / "100-superskills"
SKILLS = VENDOR / "skills"
MANIFEST = VENDOR / "KOSIF_INTEGRATION.json"
DATA = SK / "data" / "superskills.json"
UPSTREAM = "https://github.com/kosif199022-jpg/100-superskills"

TEXT_EXT = {".md", ".py", ".json", ".js", ".mjs", ".cjs", ".html", ".txt", ".css", ".sh", ".bat",
            ".yaml", ".yml", ".svg", ".toml", ".cfg", ".ini", ".csv", ".ts", ".tsx", ".jsx", ".xml",
            ".glsl", ".frag", ".vert", ""}
MAX_TEXT = 1_000_000      # bytes; larger text files (bundles) are left upstream
MAX_BINARY = 512_000      # bytes; small fonts (OFL), sound effects and images are copied
SKIP_PARTS = {"__pycache__", ".git", "node_modules", "out", "outputs", ".cache"}
SKIP_NAMES = {".DS_Store", "Thumbs.db"}
SKIP_SUFFIX = {".pyc", ".mp4", ".webm", ".mov", ".mp3"}   # repo rule (tests/test_superpowers.py): no rendered media in the skill
# Small WAV sound effects are kept, but re-encoded losslessly to FLAC (the same rule bans .wav files).
FLAC_FROM = {".wav"}

# README section heading -> domain id (the 110 catalogued skills), plus the four KOSIF core skills.
DOMAINS = [
    ("motion", "الحركة والأنيميشن", "Motion & Animation"),
    ("image-video", "الصورة والفيديو والسينما", "Image, Video & Cinema"),
    ("prompts-ai", "البرومبتات والذكاء الاصطناعي", "Prompts & AI"),
    ("office-data", "أدوات Office والبيانات", "Office & Data"),
    ("web-code", "تصميم المواقع والبرمجة", "Web Design & Programming"),
    ("business", "الكتابة والصوت والأعمال والتعليم والقرار", "Writing, Audio, Business, Learning & Decisions"),
    ("ultra", "الدفعة المتقدمة جداً", "Ultra-Advanced: Editing, Prompts, Motion & Excel"),
    ("pixel", "الرسم بالبيكسل", "Pixel Drawing Studio"),
    ("hyperframes", "الأنيميشن الاحترافي", "HyperFrames Animation Studio"),
    ("kosif-core", "مهارات KOSIF الأساسية", "KOSIF core skills"),
]
# The four KOSIF core skills have no CATALOG.json entry: their titles and Arabic search words live here.
CORE = {
    "kosif-one": ("كوسيف ون: طلب واحد وتوزيع تلقائي", "KOSIF One",
                  "الباب الواحد لكل مهارات KOSIF: طلب واحد يُخطط ويوزّع على المونتاج والموشن والبكسل والسوشيال "
                  "ويسلّم نتيجة واحدة مفحوصة. فيديو مونتاج ريل موشن انيميشن تحميل بنترست تيك توك يوتيوب صورة لوجو غلاف صوت برومبت"),
    "kosif-social": ("كوسيف سوشيال: طبقة السوشيال ميديا", "KOSIF Social",
                     "كابشن وهاشتاجات لكل منصة، عنوان ووصف يوتيوب، كاروسيل إنستجرام وتيك توك ولينكدإن PNG وPDF بعربية صحيحة، "
                     "خطة محتوى وتقويم نشر، أحسن وقت نشر، اختبار A/B"),
    "kosif-mimic": ("كوسيف ميمك: محاكاة فيديو مرجعي", "KOSIF Mimic",
                    "إعادة بناء فيديو مرجعي بلقطات جديدة مع نفس الصوت ونفس النص والخطوط والمواضع والألوان ونفس حركة النص "
                    "ونفس الانتقالات بنفس التوقيت ونفس مزاج الألوان، ولقطات مشابهة من بنترست، تقليد ريل"),
    "kosif-montage-motion": ("كوسيف مونتاج وموشن", "KOSIF Montage & Motion",
                             "موشن جرافيك ومونتاج عربي من طلب واحد: أفلام موشن 2D و3D وتايبوغرافي عربي متحرك، محاكاة ريل لقطة بلقطة، "
                             "خط زمني JSON إلى فيلم بانتقالات وتسريع وعناوين عربية وموسيقى مخفوضة، ريلز تلقائية، فيديو كلمات أغنية"),
}


# ---------------------------------------------------------------- helpers

def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def frontmatter(text: str) -> dict:
    """Tiny YAML-frontmatter reader: top-level `key: value` pairs and one nested `metadata:` level."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    out: dict = {}
    if not m:
        return out
    cur = None
    for line in m.group(1).splitlines():
        if not line.strip():
            continue
        nested = line.startswith((" ", "\t"))
        k, sep, v = line.strip().partition(":")
        if not sep:
            continue
        v = v.strip()
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
            v = v[1:-1]
        if nested and cur is not None:
            out.setdefault(cur, {})
            if isinstance(out[cur], dict):
                out[cur][k.strip()] = v
        else:
            cur = k.strip()
            out[cur] = v if v else {}
    return out


_AR_MAP = str.maketrans({"أ": "ا", "إ": "ا", "آ": "ا", "ة": "ه", "ى": "ي", "ؤ": "و", "ئ": "ي", "ـ": ""})
_DIAC = re.compile(r"[ً-ْٰ]")


def norm(s: str) -> str:
    s = _DIAC.sub("", (s or "").lower()).translate(_AR_MAP)
    return re.sub(r"[^\w؀-ۿ]+", " ", s).strip()


STOP = {"the", "a", "an", "and", "or", "to", "of", "for", "in", "on", "with", "my", "me", "i", "is", "it",
        "من", "في", "على", "الى", "عن", "مع", "و", "او", "ده", "دي", "عايز", "عاوز", "اعمل", "لي", "انا",
        "ممكن", "عشان", "علشان", "يا", "هذا", "هذه", "ان", "اللي", "بتاع", "please", "make", "want", "need"}


_PREFIX = re.compile(r"^(?:وبال|وال|بال|فال|كال|لل|ال|و)(?=\S{3,})")


def stem_words(s: str) -> str:
    """Drop the Arabic article and joined و/ب/ل prefixes from every word so «والعقود» matches «عقود»."""
    return " ".join(_PREFIX.sub("", w) for w in norm(s).split())


def terms(s: str) -> list:
    out = []
    for t in norm(s).split():
        if t in STOP or len(t) < 2:
            continue
        t = _PREFIX.sub("", t)
        out.append(t)
    return out


def rel(p: Path) -> str:
    return p.as_posix()


# ---------------------------------------------------------------- KOSIF patches (re-applied on every sync)
# Small, idempotent fixes so a vendored skill works where it now lives. Each one is listed in the
# manifest under kosif_patches; the upstream text is otherwise untouched.
PATCHES = [
    {
        "slug": "kosif-one", "file": "scripts/plan.py",
        "why": "find sibling super skills next to this folder (vendor/100-superskills/skills or ~/.claude/skills) "
               "instead of only the owner's Windows Desktop path",
        "old": 'SUPER = Path(os.environ.get("KOSIF_SUPERSKILLS", HOME / "Desktop" / "الاداة" / "100-superskills" / "skills"))\n',
        "new": ('_SIBLINGS = Path(__file__).resolve().parents[2]\n'
                'SUPER = Path(os.environ.get("KOSIF_SUPERSKILLS") or (\n'
                '    _SIBLINGS if (_SIBLINGS / "kosif-social" / "SKILL.md").is_file()\n'
                '    else HOME / "Desktop" / "الاداة" / "100-superskills" / "skills"))\n'),
    },
    {
        "slug": "kosif-one", "file": "scripts/plan.py",
        "why": "a skill that is not installed in ~/.claude/skills but sits beside kosif-one still resolves (with its path)",
        "old": ('    name = ref.split(":")[0].split(" ")[0]\n'
                '    p = SKILLS / name / "SKILL.md"\n'
                '    return {"ref": ref, "how": "Skill tool", "exists": p.exists()}\n'),
        "new": ('    name = ref.split(":")[0].split(" ")[0]\n'
                '    p = SKILLS / name / "SKILL.md"\n'
                '    if not p.exists() and (SUPER / name / "SKILL.md").exists():\n'
                '        p = SUPER / name / "SKILL.md"\n'
                '        return {"ref": ref, "how": "Skill tool", "path": str(p), "exists": True}\n'
                '    return {"ref": ref, "how": "Skill tool", "exists": p.exists()}\n'),
    },
    {
        "slug": "kosif-one", "file": "tests/test_plan.py",
        "why": "installed-skill check accepts the sibling folder; skills from other packages (ultra-motion-montage, "
               "motion-os) are skipped when absent instead of failing",
        "old": ('        for name in ("kosif-montage-motion", "hyperframes-animation-studio", "ultra-motion-montage",\n'
                '                     "motion-os", "pixel-studio-painter", "kosif-social"):\n'
                '            self.assertTrue((plan.SKILLS / name / "SKILL.md").exists(), name)\n'),
        "new": ('        for name in ("kosif-montage-motion", "hyperframes-animation-studio", "pixel-studio-painter", "kosif-social"):\n'
                '            self.assertTrue(plan.resolve(name)["exists"], name)\n'
                '        for name in ("ultra-motion-montage", "motion-os"):   # separate packages, optional here\n'
                '            if not plan.resolve(name)["exists"]:\n'
                '                print(f"skip: {name} is not installed")\n'),
    },
]


PATCHES.append({
    "slug": "pixel-studio-painter", "file": "scripts/tests/test_studio.py",
    "why": "the Motion test class needs a scripts/motion/ folder that the upstream package never shipped "
           "(KOSIF Motion lives in hyperframes-animation-studio); skip it with that reason instead of 5 errors",
    "old": 'class Motion(unittest.TestCase):\n',
    "new": ('@unittest.skipUnless((HERE / "motion" / "motion.py").is_file(),\n'
            '                     "scripts/motion/ is not shipped in this package (see hyperframes-animation-studio)")\n'
            'class Motion(unittest.TestCase):\n'),
})

PATCHES.append({
    "slug": "kosif-montage-motion", "file": "scripts/ffprobe_shim.py",
    "why": "ffmpeg 6+ prints no frame= line for a stream-copy pass, so nb_frames was missing; fall back to a decode pass",
    "old": ('    hits = re.findall(r"frame=\\s*(\\d+)", r.stderr or "")\n'
            '    return hits[-1] if hits else None\n'),
    "new": ('    hits = re.findall(r"frame=\\s*(\\d+)", r.stderr or "")\n'
            '    if not hits:   # ffmpeg 6+ prints no frame= line for a stream-copy pass: decode instead\n'
            '        r = subprocess.run([ffmpeg_exe(), "-hide_banner", "-nostdin", "-i", path, "-map", f"0:{index}", "-f", "null", "-"],\n'
            '                           capture_output=True, text=True, encoding="utf-8", errors="replace")\n'
            '        hits = re.findall(r"frame=\\s*(\\d+)", r.stderr or "")\n'
            '    return hits[-1] if hits else None\n'),
})

PATCHES.append({
    "slug": "kosif-montage-motion", "file": "scripts/kit/sfx/catalog.json",
    "why": "the six key-*.wav clicks are stored as lossless FLAC here (no .wav files in the skill), so the catalog names the .flac files",
    "old": '"file": "key-1.wav"',
    "new": '"file": "key-1.flac"',
})
PATCHES.append({
    "slug": "kosif-montage-motion", "file": "scripts/build_package.py",
    "why": "the FLAC copies of the key clicks are full-package-only sound effects like the .ogg and .wav ones",
    "old": 'rel.suffix.lower() in (".ogg", ".wav"):',
    "new": 'rel.suffix.lower() in (".ogg", ".wav", ".flac"):',
})
for _i in range(2, 7):
    PATCHES.append({"slug": "kosif-montage-motion", "file": "scripts/kit/sfx/catalog.json",
                    "why": f"key-{_i}.wav stored as lossless FLAC", "old": f'"file": "key-{_i}.wav"', "new": f'"file": "key-{_i}.flac"'})


def apply_patches(root: Path) -> list:
    done = []
    for pt in PATCHES:
        f = root / pt["slug"] / pt["file"]
        if not f.is_file():
            continue
        text = f.read_text(encoding="utf-8")
        if pt["new"] in text:
            done.append({k: pt[k] for k in ("slug", "file", "why")})
            continue
        if pt["old"] not in text:
            print(f"patch did not apply: {pt['slug']}/{pt['file']} ({pt['why'][:60]})", file=sys.stderr)
            continue
        f.write_text(text.replace(pt["old"], pt["new"], 1), encoding="utf-8")
        done.append({k: pt[k] for k in ("slug", "file", "why")})
    return done


# ---------------------------------------------------------------- sync (owner action, needs the source checkout)

def keep(path: Path, size: int) -> tuple:
    parts = set(path.parts)
    if parts & SKIP_PARTS or path.name in SKIP_NAMES or path.name.startswith(".env"):
        return False, "skipped-path"
    suf = path.suffix.lower()
    if suf in SKIP_SUFFIX:
        return False, "video-left-upstream"
    if suf in FLAC_FROM:
        return (True, "to-flac") if size <= MAX_BINARY else (False, "large-audio-left-upstream")
    if suf in TEXT_EXT:
        return (True, "text") if size <= MAX_TEXT else (False, "large-text-left-upstream")
    return (True, "binary") if size <= MAX_BINARY else (False, "large-binary-left-upstream")


def cmd_sync(a) -> int:
    src = Path(a.src).expanduser().resolve()
    if not (src / "skills").is_dir() or not (src / "CATALOG.json").is_file():
        print(f"not a 100-superskills checkout: {src}", file=sys.stderr)
        return 2
    commit = ""
    try:
        commit = subprocess.run(["git", "-C", str(src), "rev-parse", "HEAD"], capture_output=True,
                                text=True, check=True).stdout.strip()
    except Exception:
        pass
    if SKILLS.exists():
        shutil.rmtree(SKILLS)
    SKILLS.mkdir(parents=True)
    entries = []
    for sdir in sorted(p for p in (src / "skills").iterdir() if p.is_dir()):
        files, left = [], []
        for p in sorted(sdir.rglob("*")):
            if not p.is_file():
                continue
            r = p.relative_to(sdir)
            ok, why = keep(r, p.stat().st_size)
            if not ok:
                if why != "skipped-path":
                    left.append({"path": rel(r), "bytes": p.stat().st_size, "reason": why})
                continue
            dst = SKILLS / sdir.name / r
            dst.parent.mkdir(parents=True, exist_ok=True)
            if why == "to-flac":
                ff = shutil.which("ffmpeg")
                if not ff:
                    left.append({"path": rel(r), "bytes": p.stat().st_size, "reason": "wav-needs-ffmpeg-to-convert"})
                    continue
                dst = dst.with_suffix(".flac")
                subprocess.run([ff, "-nostdin", "-v", "error", "-y", "-i", str(p), "-map_metadata", "-1",
                                "-fflags", "+bitexact", "-flags:a", "+bitexact", "-c:a", "flac", str(dst)], check=True)
                r = r.with_suffix(".flac")
            else:
                shutil.copyfile(p, dst)
            os.chmod(dst, 0o644)
            files.append({"path": rel(r)})
        entries.append({"slug": sdir.name, "path": f"skills/{sdir.name}", "files": files,
                        "left_upstream": left,
                        "upstream": f"{UPSTREAM}/tree/{commit or 'main'}/skills/{sdir.name}"})
    patches = apply_patches(SKILLS)
    for e in entries:
        for f in e["files"]:
            dst = SKILLS / e["slug"] / f["path"]
            f["sha256"], f["bytes"] = sha256(dst), dst.stat().st_size
    for name in ("LICENSE", "CATALOG.json", "README.md", "TESTS.md", "INSTALL.ar.md"):
        if (src / name).is_file():
            shutil.copyfile(src / name, VENDOR / name)
            os.chmod(VENDOR / name, 0o644)
    man = {
        "name": "100 Super Skills (owner repository) vendored into KOSIF Superpowers",
        "master_skill": "kosif-superpowers",
        "upstream": UPSTREAM,
        "upstream_commit": commit,
        "upstream_license": "MIT (c) 2026 Kosif; each skill's references/sources.md names the permissive sources it was composed from",
        "integration_mode": "whole skill folders copied (text, plus small OFL fonts, sound effects and images); "
                            "large media and bundles stay upstream and are listed per skill under left_upstream",
        "policy": f"text <= {MAX_TEXT} bytes, binary <= {MAX_BINARY} bytes, no video, no caches; files are not executable; "
                  "KOSIF runs nothing here except each skill's own tests in a temporary copy (selftest)",
        "kosif_patches": patches,
        "skills_count": len(entries),
        "skills": entries,
    }
    MANIFEST.write_text(json.dumps(man, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    n_files = sum(len(e["files"]) for e in entries)
    n_left = sum(len(e["left_upstream"]) for e in entries)
    print(json.dumps({"skills": len(entries), "files": n_files, "left_upstream": n_left, "commit": commit[:12]}))
    return cmd_build(a)


# ---------------------------------------------------------------- build data/superskills.json

def readme_domains(readme: str) -> dict:
    """slug -> (domain id, number) from the README tables and bullet list."""
    out, dom = {}, None
    for line in readme.splitlines():
        if line.startswith("### "):
            dom = None
            for did, ar, en in DOMAINS:
                if ar in line or en.split(":")[0] in line:
                    dom = did
                    break
        m = re.search(r"\(skills/([a-z0-9-]+)/SKILL\.md\)", line)
        if m and dom and m.group(1) not in out:
            num = re.match(r"\|\s*(\d+)\s*\|", line)
            out[m.group(1)] = (dom, num.group(1) if num else "")
    return out


def build_records() -> dict:
    man = json.loads(MANIFEST.read_text(encoding="utf-8"))
    cat = {}
    if (VENDOR / "CATALOG.json").is_file():
        cat = {c["slug"]: c for c in json.loads((VENDOR / "CATALOG.json").read_text(encoding="utf-8"))}
    doms = readme_domains((VENDOR / "README.md").read_text(encoding="utf-8")) if (VENDOR / "README.md").is_file() else {}
    recs = []
    for e in man["skills"]:
        slug = e["slug"]
        sdir = VENDOR / e["path"]
        fm = frontmatter((sdir / "SKILL.md").read_text(encoding="utf-8"))
        meta = fm.get("metadata") if isinstance(fm.get("metadata"), dict) else {}
        c = cat.get(slug, {})
        paths = [f["path"] for f in e["files"]]
        scripts = sorted(p for p in paths if p.endswith((".py", ".mjs", ".cjs", ".js"))
                         and ("scripts/" in p or "/" not in p) and "/tests/" not in p and not p.startswith("tests/")
                         and "/static/" not in p and "/projects/" not in p and not p.endswith(".bundle.js"))
        tests = sorted({str(Path(p).parent) for p in paths
                        if re.search(r"(^|/)test_[^/]+\.py$", p)})
        dom, num = ("kosif-core", "") if slug in CORE else doms.get(slug, ("misc", ""))
        licenses = sorted({s.get("license", "") for s in c.get("sources", []) if s.get("license")})
        recs.append({
            "slug": slug,
            "n": c.get("n") or num or str(meta.get("superskill", "")),
            "domain": dom,
            "title_ar": c.get("ar") or meta.get("title_ar", "") or CORE.get(slug, ("",))[0],
            "title_en": c.get("en") or (CORE[slug][1] if slug in CORE else fm.get("name", slug)),
            "description": fm.get("description", "") if isinstance(fm.get("description"), str) else "",
            "summary_ar": c.get("desc", "") or (CORE[slug][2] if slug in CORE else ""),
            "path": f"vendor/100-superskills/{e['path']}",
            "files": len(paths),
            "bytes": sum(f["bytes"] for f in e["files"]),
            "scripts": scripts,
            "test_dirs": tests,
            "left_upstream": [x["path"] for x in e.get("left_upstream", [])],
            "source_licenses": licenses,
            "sources": [s.get("name") for s in c.get("sources", [])][:8],
            "install": f"python3 scripts/superskills.py install {slug}",
        })
    recs.sort(key=lambda r: ([d[0] for d in DOMAINS] + ["misc"]).index(r["domain"]) * 1000 + int(r["n"] or 999))
    return {
        "schema": "kosif.superskills.v1",
        "upstream": man["upstream"],
        "upstream_commit": man.get("upstream_commit", ""),
        "count": len(recs),
        "domains": [{"id": d, "ar": ar, "en": en, "count": sum(r["domain"] == d for r in recs)} for d, ar, en in DOMAINS],
        "skills": recs,
    }


def cmd_build(a) -> int:
    data = build_records()
    text = json.dumps(data, ensure_ascii=False, indent=1) + "\n"
    if getattr(a, "check", False):
        cur = DATA.read_text(encoding="utf-8") if DATA.is_file() else ""
        if cur != text:
            print("data/superskills.json is stale: run python3 scripts/superskills.py build", file=sys.stderr)
            return 1
        print(f"ok: {data['count']} super skills, data/superskills.json up to date")
        return 0
    DATA.write_text(text, encoding="utf-8")
    print(f"wrote data/superskills.json: {data['count']} skills in {sum(1 for d in data['domains'] if d['count'])} domains")
    return 0


# ---------------------------------------------------------------- read side

def load() -> dict:
    if not DATA.is_file():
        raise SystemExit("data/superskills.json is missing: run python3 scripts/superskills.py build")
    return json.loads(DATA.read_text(encoding="utf-8"))


def score(rec: dict, ts: list) -> float:
    if not ts:
        return 0.0
    slug = norm(rec["slug"].replace("-", " "))
    title = stem_words(rec["title_ar"] + " " + rec["title_en"])
    body = stem_words(rec["description"] + " " + rec["summary_ar"])
    s = 0.0
    for t in ts:
        if t in slug.split():
            s += 4
        elif t in slug:
            s += 2.5
        if re.search(rf"(^| ){re.escape(t)}", title):
            s += 3
        n = len(re.findall(rf"(^| ){re.escape(t)}", body))
        s += min(n, 3) * 1.0
    return s / (len(ts) ** 0.5)


def find(brief: str, limit: int = 5) -> list:
    data, ts = load(), terms(brief)
    ranked = sorted(((score(r, ts), r) for r in data["skills"]), key=lambda x: (-x[0], x[1]["slug"]))
    return [(round(sc, 2), r) for sc, r in ranked if sc > 0][:limit]


def cmd_find(a) -> int:
    hits = find(a.brief, a.limit)
    if a.json:
        print(json.dumps([{"score": s, "slug": r["slug"], "title_ar": r["title_ar"], "title_en": r["title_en"],
                           "domain": r["domain"], "path": r["path"], "scripts": len(r["scripts"]),
                           "show": f"python3 scripts/superskills.py show {r['slug']}"} for s, r in hits],
                         ensure_ascii=False, indent=1))
        return 0 if hits else 1
    if not hits:
        print("no super skill matched; try other words or `list`")
        return 1
    for s, r in hits:
        print(f"{s:5.2f}  {r['slug']:<34} {r['title_ar']} / {r['title_en']}  [{r['domain']}, {len(r['scripts'])} scripts]")
    print(f"\nread one: python3 scripts/superskills.py show {hits[0][1]['slug']}")
    return 0


def cmd_list(a) -> int:
    data = load()
    for d in data["domains"]:
        if a.domain and d["id"] != a.domain:
            continue
        rows = [r for r in data["skills"] if r["domain"] == d["id"]]
        if not rows:
            continue
        print(f"\n## {d['ar']} — {d['en']} ({len(rows)})")
        for r in rows:
            print(f"  {r['n'] or '--':>3}  {r['slug']:<34} {r['title_ar']}")
    print(f"\n{data['count']} super skills from {data['upstream']}")
    return 0


def get(slug: str) -> dict:
    for r in load()["skills"]:
        if r["slug"] == slug:
            return r
    close = [h[1]["slug"] for h in find(slug.replace("-", " "), 3)]
    raise SystemExit(f"unknown super skill: {slug}" + (f" (did you mean {', '.join(close)}?)" if close else ""))


def cmd_show(a) -> int:
    r = get(a.slug)
    present = (SK / r["path"] / "SKILL.md").is_file()
    if a.json:
        print(json.dumps(dict(r, vendored_here=present), ensure_ascii=False, indent=1))
        return 0
    print(f"# {r['title_ar']} — {r['title_en']}  ({r['slug']}, #{r['n'] or '-'}, {r['domain']})\n")
    print(r["description"] or r["summary_ar"])
    print(f"\npath: .claude/skills/kosif-superpowers/{r['path']}/SKILL.md" + ("" if present else
          "  (not in this package: vendor/ is left out of the claude.ai zip; see upstream)"))
    if r["scripts"]:
        print(f"scripts ({len(r['scripts'])}): " + ", ".join(r["scripts"][:12]) + (" …" if len(r["scripts"]) > 12 else ""))
    if r["test_dirs"]:
        print("tests: " + ", ".join(r["test_dirs"]) + f"   (python3 scripts/superskills.py selftest {r['slug']})")
    if r["source_licenses"]:
        print("composed from: " + ", ".join(r["sources"]) + "  [" + ", ".join(r["source_licenses"]) + "]")
    if r["left_upstream"]:
        print(f"left upstream ({len(r['left_upstream'])} large media files): {UPSTREAM}/tree/main/skills/{r['slug']}")
    print(f"install for direct use: {r['install']}")
    if a.full and present:
        print("\n" + "-" * 60 + "\n" + (SK / r["path"] / "SKILL.md").read_text(encoding="utf-8"))
    return 0


def cmd_install(a) -> int:
    r = get(a.slug)
    src = SK / r["path"]
    if not (src / "SKILL.md").is_file():
        print(f"{r['slug']} is not vendored in this copy; get it from {UPSTREAM}", file=sys.stderr)
        return 2
    dest = Path(os.path.expanduser(a.dest)) / r["slug"]
    if dest.exists() and not a.force:
        print(f"{dest} exists; pass --force to replace it (a .bak copy is kept)", file=sys.stderr)
        return 2
    if a.dry_run:
        print(f"would copy {src} -> {dest} ({r['files']} files)")
        return 0
    if dest.exists():
        bak = dest.with_name(dest.name + f".bak-{time.strftime('%Y%m%d%H%M%S')}")
        shutil.move(str(dest), str(bak))
        print(f"kept the old copy at {bak}")
    shutil.copytree(src, dest)
    print(f"installed {r['slug']} -> {dest}")
    if r["left_upstream"]:
        print(f"note: {len(r['left_upstream'])} large media files stay upstream: {UPSTREAM}/tree/main/skills/{r['slug']}")
    return 0


def cmd_verify(a) -> int:
    man = json.loads(MANIFEST.read_text(encoding="utf-8"))
    bad, n = [], 0
    for e in man["skills"]:
        for f in e["files"]:
            p = VENDOR / e["path"] / f["path"]
            n += 1
            if not p.is_file() or sha256(p) != f["sha256"]:
                bad.append(f"{e['slug']}/{f['path']}")
    listed = {(e["slug"], f["path"]) for e in man["skills"] for f in e["files"]}
    extra = [rel(p.relative_to(SKILLS)) for p in SKILLS.rglob("*") if p.is_file()
             and "__pycache__" not in p.parts
             and (p.relative_to(SKILLS).parts[0], rel(p.relative_to(SKILLS / p.relative_to(SKILLS).parts[0]))) not in listed]
    print(json.dumps({"skills": man["skills_count"], "files": n, "mismatched": bad[:20], "unlisted": extra[:20],
                      "ok": not bad and not extra}, ensure_ascii=False))
    return 0 if not bad and not extra else 1


def cmd_selftest(a) -> int:
    data = load()
    want = set(a.slugs)
    rows = [r for r in data["skills"] if r["test_dirs"] and (not want or r["slug"] in want)]
    if want - {r["slug"] for r in rows}:
        print("no tests for: " + ", ".join(sorted(want - {r['slug'] for r in rows})), file=sys.stderr)
    results, worst = [], 0
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    with tempfile.TemporaryDirectory(prefix="superskills-") as tmp:
        # the whole skills folder is copied, because some skills (kosif-one) look for their siblings
        root = Path(tmp) / "skills"
        shutil.copytree(SKILLS, root)
        for r in rows:
            dst = root / r["slug"]
            for td in r["test_dirs"]:
                start = dst / td
                t0 = time.time()
                try:
                    p = subprocess.run([sys.executable, "-B", "-m", "unittest", "discover", "-s", start.name],
                                       cwd=str(start.parent), capture_output=True, text=True,
                                       timeout=a.timeout, env=env)
                    tail = (p.stderr or p.stdout).strip().splitlines()[-1:] or [""]
                    m = re.search(r"Ran (\d+) test", p.stderr or "")
                    status = "passed" if p.returncode == 0 else "failed"
                    results.append({"slug": r["slug"], "dir": td, "status": status, "ran": int(m.group(1)) if m else 0,
                                    "seconds": round(time.time() - t0, 1), "last_line": tail[0][:160]})
                    worst = max(worst, p.returncode != 0)
                except subprocess.TimeoutExpired:
                    results.append({"slug": r["slug"], "dir": td, "status": "timeout", "ran": 0,
                                    "seconds": a.timeout, "last_line": ""})
                    worst = 1
    if a.json:
        print(json.dumps(results, ensure_ascii=False, indent=1))
    else:
        for x in results:
            print(f"{x['status']:<8} {x['slug']}/{x['dir']}  ran={x['ran']}  {x['seconds']}s  {x['last_line']}")
    return worst


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("sync"); p.add_argument("--src", required=True); p.set_defaults(fn=cmd_sync, check=False)
    p = sub.add_parser("build"); p.add_argument("--check", action="store_true"); p.set_defaults(fn=cmd_build)
    p = sub.add_parser("list"); p.add_argument("--domain"); p.set_defaults(fn=cmd_list)
    p = sub.add_parser("find"); p.add_argument("brief"); p.add_argument("--limit", type=int, default=5)
    p.add_argument("--json", action="store_true"); p.set_defaults(fn=cmd_find)
    p = sub.add_parser("show"); p.add_argument("slug"); p.add_argument("--json", action="store_true")
    p.add_argument("--full", action="store_true", help="also print the whole SKILL.md"); p.set_defaults(fn=cmd_show)
    p = sub.add_parser("install"); p.add_argument("slug"); p.add_argument("--dest", default="~/.claude/skills")
    p.add_argument("--force", action="store_true"); p.add_argument("--dry-run", action="store_true")
    p.set_defaults(fn=cmd_install)
    p = sub.add_parser("verify"); p.set_defaults(fn=cmd_verify)
    p = sub.add_parser("selftest"); p.add_argument("slugs", nargs="*"); p.add_argument("--timeout", type=int, default=300)
    p.add_argument("--json", action="store_true"); p.set_defaults(fn=cmd_selftest)
    a = ap.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
