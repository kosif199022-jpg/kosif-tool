#!/usr/bin/env python3
"""KOSIF superpowers catalog CLI — فهرس القوى: list, search, show, doctor, stats, build, check.

The catalog (`repos.json` next to this skill) records 100 major open-source repositories
whose capabilities a KOSIF film-maker can draw on, grouped into twelve superpowers.
This tool reads it, regenerates `references/repos.md` from it and checks which of the
tools are actually installed on this machine — so a plan never promises an integration
that is not there.

  python3 superpowers.py list [--capability KEY] [--domain KEY] [--license-note TEXT] [--json]
  python3 superpowers.py search <words...> [--json]
  python3 superpowers.py show <owner/repo> [--json]
  python3 superpowers.py doctor [--json] [--strict]
  python3 superpowers.py stats
  python3 superpowers.py build [--check]
  python3 superpowers.py check            # validate repos.json + derived repos.md (CI/tests)
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import shutil
import signal
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent                     # .claude/skills/kosif-superpowers
REPO = SKILL.parents[2]                 # repository root
DATA = SKILL / "repos.json"
REPOS_MD = SKILL / "references" / "repos.md"
ARABIC = re.compile(r"[؀-ۿ]")

CAP_ORDER = ["observe", "animate", "render", "space", "draw", "data", "voice", "arabic", "captions", "generate", "orchestrate", "design", "mimic", "edit", "cinematic"]
CAP_AR = {
    "observe": "رصد المرجع", "animate": "التحريك", "render": "الرندر", "space": "الفضاء ثلاثي الأبعاد",
    "draw": "الرسم", "data": "البيانات", "voice": "الصوت", "arabic": "النص العربي", "captions": "الترجمات",
    "generate": "التوليد", "orchestrate": "التنسيق", "design": "التصميم",
    "mimic": "المحاكاة", "edit": "المونتاج", "cinematic": "الإخراج السينمائي",
}
LICENSE_NOTES = (
    "permissive",
    "weak copyleft",
    "copyleft: run as an external tool, do not vendor",
    "model/weights license: check commercial terms",
    "custom: read before use",
    "unknown",
)
REQUIRED = ("owner_repo", "url", "name", "stars_k", "license", "license_note", "summary_en", "summary_ar",
            "capability", "domain", "kosif_use_en", "kosif_use_ar", "integration_en", "playbooks", "caveats_en")
EXPECTED_COUNT = 100


class CliError(Exception):
    pass


# -- data ---------------------------------------------------------------------------
def load() -> dict:
    if not DATA.exists():
        raise CliError(f"الفهرس غير موجود / catalog missing: {DATA}")
    try:
        return json.loads(DATA.read_text(encoding="utf-8"))
    except ValueError as exc:
        raise CliError(f"repos.json is not valid JSON: {exc}")


def norm(owner_repo: str) -> str:
    return owner_repo.strip().lower().rstrip("/")


def validate(data: dict, root: Path = REPO) -> list[str]:
    """Return a list of problems; empty when the catalog is sound."""
    problems: list[str] = []
    repos = data.get("repos")
    caps = data.get("capabilities") or {}
    domains = {d.get("key") for d in data.get("domains") or []}
    if not isinstance(repos, list):
        return ["repos must be a list"]
    if len(repos) != EXPECTED_COUNT:
        problems.append(f"expected {EXPECTED_COUNT} repositories, found {len(repos)}")
    seen: set[str] = set()
    for i, r in enumerate(repos):
        tag = f"#{i + 1} {r.get('owner_repo', '?')}"
        for key in REQUIRED:
            if key not in r or r[key] in ("", None):
                problems.append(f"{tag}: missing {key}")
        owner_repo = str(r.get("owner_repo", ""))
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", owner_repo):
            problems.append(f"{tag}: owner_repo must look like owner/name")
        if norm(owner_repo) in seen:
            problems.append(f"{tag}: duplicate owner_repo")
        seen.add(norm(owner_repo))
        if r.get("url") != f"https://github.com/{owner_repo}":
            problems.append(f"{tag}: url must be https://github.com/{owner_repo}")
        if not isinstance(r.get("stars_k"), (int, float)) or r.get("stars_k", -1) < 0:
            problems.append(f"{tag}: stars_k must be a non-negative number (thousands)")
        if r.get("license_note") not in LICENSE_NOTES:
            problems.append(f"{tag}: license_note must be one of {LICENSE_NOTES}")
        if r.get("capability") not in caps:
            problems.append(f"{tag}: unknown capability {r.get('capability')!r}")
        if r.get("domain") not in domains:
            problems.append(f"{tag}: unknown domain {r.get('domain')!r}")
        if not ARABIC.search(str(r.get("summary_ar", ""))) or not ARABIC.search(str(r.get("kosif_use_ar", ""))):
            problems.append(f"{tag}: summary_ar and kosif_use_ar must be Arabic")
        if not isinstance(r.get("playbooks"), list):
            problems.append(f"{tag}: playbooks must be a list")
        else:
            for p in r["playbooks"]:
                if not re.fullmatch(r"playbooks/[a-z0-9-]+\.md", str(p)) or not (root / p).exists():
                    problems.append(f"{tag}: playbook {p!r} does not exist")
    for cap in caps:
        if cap not in CAP_AR:
            problems.append(f"capability {cap!r} has no Arabic title in superpowers.py")
    return problems


# -- rendering -------------------------------------------------------------------------
def md_cell(text) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ").strip()


def render_repos_md(data: dict) -> str:
    repos = data["repos"]
    caps = data.get("capabilities") or {}
    domains = {d["key"]: d for d in data.get("domains") or []}
    stars = sum(float(r.get("stars_k") or 0) for r in repos)
    notes = Counter(r.get("license_note") for r in repos)
    used_caps = [c for c in caps if any(r["capability"] == c for r in repos)]
    out = [
        "# Superpowers repository catalog — فهرس مستودعات القوى",
        "",
        "Generated from `repos.json` by `python3 .claude/skills/kosif-superpowers/scripts/superpowers.py build`; do not edit by hand.",
        "يُولَّد هذا الملف من `repos.json`؛ لا تحرّره يدويًا.",
        "",
        f"**{len(repos)}** repositories · **{len(used_caps)}** superpowers · ≈ **{stars:,.0f}k** GitHub stars combined · generated {data.get('generated', '')}",
        "",
        "## How to read — كيفية القراءة",
        "",
        "Each row is a capability a KOSIF film-maker may call on, with the exact way to invoke it and the KOSIF playbooks it strengthens. Links point to the owners' repositories; nothing is vendored or copied. Star counts are rounded thousands at generation time.",
        "",
        "**بالعربية:** كل صف قدرة يمكن لصانع فيلم KOSIF الاستعانة بها، مع طريقة الاستدعاء والدلائل التي تعززها. الروابط تشير إلى مستودعات أصحابها؛ لا شيء منسوخ أو مضمَّن.",
        "",
        "License notes / ملاحظات الترخيص: " + " · ".join(f"**{k}** ({v})" for k, v in sorted(notes.items(), key=lambda kv: (-kv[1], kv[0]))),
        "",
        "- *permissive* — MIT/Apache/BSD-style: may be installed, imported and shipped with credit.",
        "- *weak copyleft* — LGPL/MPL-style: link or run as-is, publish changes to the library itself.",
        "- *copyleft: run as an external tool, do not vendor* — GPL/AGPL: call the CLI, keep its source outside your film's code.",
        "- *model/weights license: check commercial terms* — code may be open while weights carry use restrictions; read before commercial delivery.",
        "- *custom: read before use* — bespoke terms (for example proprietary plugins next to an open core).",
        "",
    ]
    for cap in CAP_ORDER + [c for c in caps if c not in CAP_ORDER]:
        rows = [r for r in repos if r.get("capability") == cap]
        if not rows:
            continue
        rows.sort(key=lambda r: (-float(r.get("stars_k") or 0), r["owner_repo"].lower()))
        out += [f"## {cap} — {CAP_AR.get(cap, cap)} ({len(rows)})", "", f"{caps.get(cap, '')}", "",
                "| # | Repository | ★k | License | Gives KOSIF / ما يقدمه | Invoke | Playbooks |",
                "|---|---|---|---|---|---|---|"]
        for i, r in enumerate(rows, 1):
            dom = domains.get(r.get("domain"), {}).get("title", r.get("domain"))
            gives = f"{md_cell(r['kosif_use_en'])}<br>{md_cell(r['kosif_use_ar'])}"
            pbs = ", ".join(f"[{Path(p).stem}](../../../../{p})" for p in r.get("playbooks") or []) or "—"
            invoke = md_cell(r["integration_en"]).replace("`", "")
            out.append(f"| {i} | [{md_cell(r['name'])}]({r['url']})<br><sub>{md_cell(r['owner_repo'])} · {md_cell(dom)}</sub> | {float(r.get('stars_k') or 0):g} | {md_cell(r['license'])}<br><sub>{md_cell(r['license_note'])}</sub> | {gives} | `{invoke}` | {pbs} |")
        out.append("")
        caveats = [r for r in rows if str(r.get("caveats_en", "")).strip().lower().rstrip(".") not in ("", "none")]
        if caveats:
            out += ["<details><summary>Caveats / محاذير</summary>", ""]
            out += [f"- **{md_cell(r['name'])}** — {md_cell(r['caveats_en'])}" for r in caveats]
            out += ["", "</details>", ""]
    out += [
        "## Credits and policy — الحقوق والسياسة",
        "",
        "Every project above belongs to its authors under the license shown. KOSIF links and credits; it never redistributes third-party code, prompts, media or weights. When a recipe in `capabilities.md` uses one of these tools, install it from its own repository and keep its license notice.",
        "",
        "**بالعربية:** كل مشروع أعلاه ملك لأصحابه بترخيصه المبيّن. KOSIF يربط وينسب الفضل ولا يعيد توزيع كود أو نصوص أو وسائط أو أوزان لطرف ثالث.",
        "",
    ]
    return "\n".join(out)


# -- commands ---------------------------------------------------------------------------
def trunc(text: str, width: int) -> str:
    text = str(text)
    return text if len(text) <= width else text[: max(0, width - 1)] + "…"


def print_table(rows: list[list[str]], headers: list[str], widths: list[int]) -> None:
    def fmt(cells):
        return "  ".join(trunc(c, w).ljust(w) for c, w in zip(cells, widths))
    print(fmt(headers))
    print(fmt(["-" * w for w in widths]))
    for row in rows:
        print(fmt(row))


def row_for(r: dict) -> list[str]:
    return [r["owner_repo"], f"{float(r.get('stars_k') or 0):g}", r["license"], r["capability"], r["kosif_use_en"]]


HEADERS = ["owner/repo", "★k", "license", "power", "gives KOSIF"]
WIDTHS = [36, 6, 14, 11, 70]


def cmd_list(args) -> int:
    data = load()
    rows = data["repos"]
    if args.capability:
        rows = [r for r in rows if r["capability"] == args.capability]
    if args.domain:
        rows = [r for r in rows if r["domain"] == args.domain]
    if args.license_note:
        rows = [r for r in rows if args.license_note.lower() in r["license_note"].lower()]
    rows.sort(key=lambda r: (CAP_ORDER.index(r["capability"]) if r["capability"] in CAP_ORDER else 99, -float(r.get("stars_k") or 0)))
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0
    print_table([row_for(r) for r in rows], HEADERS, WIDTHS)
    print(f"\n{len(rows)} مستودع / repositories")
    return 0


def haystack(r: dict) -> str:
    return " ".join(str(r.get(k, "")) for k in ("owner_repo", "name", "summary_en", "summary_ar", "kosif_use_en", "kosif_use_ar", "integration_en", "capability", "domain", "license")).lower()


def cmd_search(args) -> int:
    data = load()
    words = [w.lower() for w in args.words if w.strip()]
    if not words:
        raise CliError("أدخل كلمة للبحث / give at least one word")
    rows = [r for r in data["repos"] if all(w in haystack(r) for w in words)]
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0 if rows else 1
    if not rows:
        print("لا نتائج / no matches")
        return 1
    print_table([row_for(r) for r in rows], HEADERS, WIDTHS)
    print(f"\n{len(rows)} نتيجة / results")
    return 0


def cmd_show(args) -> int:
    data = load()
    key = norm(args.owner_repo).replace("https://github.com/", "")
    rec = next((r for r in data["repos"] if norm(r["owner_repo"]) == key), None)
    if rec is None:
        close = [r["owner_repo"] for r in data["repos"] if key.split("/")[-1] in norm(r["owner_repo"])][:5]
        hint = f"\n  هل تقصد / did you mean: {', '.join(close)}" if close else ""
        raise CliError(f"غير موجود / not in the catalog: {args.owner_repo}{hint}")
    if args.json:
        print(json.dumps(rec, ensure_ascii=False, indent=2))
        return 0
    cap = rec["capability"]
    print(f"{rec['name']}  ({rec['owner_repo']})  ★ {float(rec.get('stars_k') or 0):g}k  {rec['license']} — {rec['license_note']}")
    print(f"  {rec['url']}")
    print(f"  القوة / superpower: {cap} — {CAP_AR.get(cap, cap)} · domain: {rec['domain']}")
    print(f"  {rec['summary_en']}\n  {rec['summary_ar']}")
    print(f"  يقدّم لـ KOSIF / gives: {rec['kosif_use_en']}\n  {rec['kosif_use_ar']}")
    print(f"  الاستدعاء / invoke: {rec['integration_en']}")
    print(f"  محاذير / caveats: {rec['caveats_en']}")
    print(f"  الدلائل / playbooks: {', '.join(rec['playbooks']) or '—'}")
    return 0


def _node_module(name: str) -> str | None:
    for base in (REPO / "node_modules", REPO / "starters" / "remotion" / "node_modules", Path("/opt/node-tools/node_modules")):
        if (base / name).exists():
            return str(base / name)
    env = os.environ.get("KOSIF_PLAYWRIGHT") if name == "playwright" else None
    return env if env and Path(env).exists() else None


def _py_module(name: str) -> str | None:
    try:
        spec = importlib.util.find_spec(name)
    except (ImportError, ValueError):
        return None
    return (spec.origin or name) if spec else None


def _chromium() -> str | None:
    base = Path(os.environ.get("PLAYWRIGHT_BROWSERS_PATH") or "/opt/pw-browsers")
    hits = sorted(base.glob("chromium*")) if base.exists() else []
    return str(hits[0]) if hits else None


DOCTOR_CHECKS = [
    # (id, label, probe, install hint) — a probe returns a path/str when the tool is present
    ("node", "Node.js (render_html.cjs, Remotion)", lambda: shutil.which("node"), "install Node 22 from nodejs.org"),
    ("python", "Python 3", lambda: sys.executable, ""),
    ("ffmpeg", "ffmpeg (encode, contact sheets, palettes)", lambda: shutil.which("ffmpeg"), "apt install ffmpeg / brew install ffmpeg"),
    ("ffprobe", "ffprobe (verify_video.py, probe.json)", lambda: shutil.which("ffprobe"), "comes with ffmpeg"),
    ("playwright", "Playwright (deterministic frame capture)", lambda: _node_module("playwright"), "npm i -D playwright (never 'playwright install' on the KOSIF cloud machine)"),
    ("chromium", "Chromium for Playwright", _chromium, "set PLAYWRIGHT_BROWSERS_PATH or run npx playwright install chromium locally"),
    ("remotion", "Remotion (starters/remotion)", lambda: _node_module("remotion"), "cd starters/remotion && npm install"),
    ("git", "git (worktrees for parallel scenes)", lambda: shutil.which("git"), ""),
    ("yt-dlp", "yt-dlp (permitted reference downloads)", lambda: shutil.which("yt-dlp"), "pip install yt-dlp"),
    ("whisper", "openai-whisper (word timestamps)", lambda: _py_module("whisper"), "pip install -U openai-whisper"),
    ("faster_whisper", "faster-whisper (CPU-friendly transcription)", lambda: _py_module("faster_whisper"), "pip install faster-whisper"),
    ("whisperx", "WhisperX (forced alignment)", lambda: _py_module("whisperx"), "pip install whisperx"),
    ("cv2", "OpenCV (frame analysis)", lambda: _py_module("cv2"), "pip install opencv-python-headless"),
    ("scenedetect", "PySceneDetect (cut detection)", lambda: _py_module("scenedetect"), "pip install scenedetect[opencv]"),
    ("PIL", "Pillow (image sampling)", lambda: _py_module("PIL"), "pip install pillow"),
    ("numpy", "NumPy", lambda: _py_module("numpy"), "pip install numpy"),
    ("arabic_reshaper", "arabic-reshaper (Arabic shaping outside browsers)", lambda: _py_module("arabic_reshaper"), "pip install arabic-reshaper python-bidi"),
    ("bidi", "python-bidi", lambda: _py_module("bidi"), "pip install python-bidi"),
    ("imagemagick", "ImageMagick (sprite sheets, GIF checks)", lambda: shutil.which("magick") or shutil.which("convert"), "apt install imagemagick"),
    ("blender", "Blender (3D renders)", lambda: shutil.which("blender"), "download from blender.org"),
    ("gpu", "NVIDIA GPU (generative models)", lambda: shutil.which("nvidia-smi"), "run GPU models elsewhere and import the result"),
]
CORE = ("node", "ffmpeg", "ffprobe", "playwright", "chromium")


def cmd_doctor(args) -> int:
    results = []
    for key, label, probe, hint in DOCTOR_CHECKS:
        try:
            where = probe()
        except Exception:  # pragma: no cover - defensive
            where = None
        results.append({"id": key, "label": label, "installed": bool(where), "where": where or "", "hint": hint, "core": key in CORE})
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for r in results:
            mark = "✓" if r["installed"] else "✗"
            tail = r["where"] if r["installed"] else (f"— {r['hint']}" if r["hint"] else "")
            print(f"{mark} {r['label']:<48} {trunc(tail, 70)}")
        n = sum(r["installed"] for r in results)
        print(f"\n{n}/{len(results)} متوفر / available. Plans may only promise what is marked ✓; for the rest say 'install first' or run elsewhere and import the result.")
    missing_core = [r["id"] for r in results if r["core"] and not r["installed"]]
    return 1 if (args.strict and missing_core) else 0


def cmd_stats(args) -> int:
    data = load()
    repos = data["repos"]
    print(f"{len(repos)} مستودع / repositories · ≈ {sum(float(r.get('stars_k') or 0) for r in repos):,.0f}k stars")
    for title, key in (("القوى / superpowers", "capability"), ("المجالات / domains", "domain"), ("الترخيص / license notes", "license_note")):
        print(f"\n{title}")
        for k, v in Counter(r[key] for r in repos).most_common():
            print(f"  {v:3}  {k}")
    return 0


def cmd_build(args) -> int:
    data = load()
    problems = validate(data)
    if problems:
        for p in problems:
            print("  !", p, file=sys.stderr)
        raise CliError(f"{len(problems)} مشكلة في repos.json / problems in repos.json")
    text = render_repos_md(data)
    if args.check:
        current = REPOS_MD.read_text(encoding="utf-8") if REPOS_MD.exists() else ""
        if current != text:
            print("references/repos.md قديم / is out of date — run: python3 .claude/skills/kosif-superpowers/scripts/superpowers.py build", file=sys.stderr)
            return 1
        print("references/repos.md محدّث / up to date")
        return 0
    REPOS_MD.parent.mkdir(parents=True, exist_ok=True)
    REPOS_MD.write_text(text, encoding="utf-8")
    print(f"كُتب / wrote {REPOS_MD.relative_to(REPO)} ({len(data['repos'])} repositories)")
    return 0


def cmd_check(args) -> int:
    data = load()
    problems = validate(data)
    for p in problems:
        print("  !", p, file=sys.stderr)
    args.check = True
    try:
        rc = cmd_build(args)
    except CliError as exc:
        print(exc, file=sys.stderr)
        rc = 1
    if problems or rc:
        print("النتيجة / result: FAIL")
        return 1
    print(f"النتيجة / result: OK — {len(data['repos'])} repositories")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="superpowers.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd")
    s = sub.add_parser("list", help="list repositories / اعرض المستودعات")
    s.add_argument("--capability", help=f"one of {', '.join(CAP_ORDER)}")
    s.add_argument("--domain")
    s.add_argument("--license-note")
    s.add_argument("--json", action="store_true")
    s.set_defaults(func=cmd_list)
    s = sub.add_parser("search", help="search names, summaries and uses (AR/EN) / ابحث")
    s.add_argument("words", nargs="+")
    s.add_argument("--json", action="store_true")
    s.set_defaults(func=cmd_search)
    s = sub.add_parser("show", help="show one record / اعرض سجلًا")
    s.add_argument("owner_repo")
    s.add_argument("--json", action="store_true")
    s.set_defaults(func=cmd_show)
    s = sub.add_parser("doctor", help="which tools are installed here / ما المتوفر على هذا الجهاز")
    s.add_argument("--json", action="store_true")
    s.add_argument("--strict", action="store_true", help="exit 1 when a core render tool is missing")
    s.set_defaults(func=cmd_doctor)
    s = sub.add_parser("stats", help="counts per superpower, domain and license / إحصاءات")
    s.set_defaults(func=cmd_stats)
    s = sub.add_parser("build", help="regenerate references/repos.md / ولّد الفهرس")
    s.add_argument("--check", action="store_true", help="only verify repos.md is up to date")
    s.set_defaults(func=cmd_build)
    s = sub.add_parser("check", help="validate repos.json and repos.md / افحص")
    s.set_defaults(func=cmd_check)
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.cmd:
        parser.print_help()
        return 0
    try:
        return args.func(args)
    except CliError as exc:
        print(f"خطأ / error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # quiet exit when piped into head
    sys.exit(main())
