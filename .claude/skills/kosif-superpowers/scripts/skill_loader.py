#!/usr/bin/env python3
"""KOSIF light skill loader — one small map instead of reading every big file (USIP v5.9).

The skill files are large (SKILL.md alone is ~80 KB). Reading them all at the start of a chat burns context and
still leaves most skills unreached. This script writes LOADER.md: a one-screen-per-section map of every skill under
.claude/skills/, the 15 capability groups, every protocol appendix with its trigger, and the line ranges of each
SKILL.md section so Claude can open just the lines it needs (sed -n START,ENDp). It also answers `need "<task>"`
with the few files and line ranges to open for one task, and prints the full-power reading order on request.

From the repository root:
  python3 .claude/skills/kosif-superpowers/scripts/skill_loader.py build          # write LOADER.md
  python3 .claude/skills/kosif-superpowers/scripts/skill_loader.py build --check  # exit 1 if LOADER.md is stale
  python3 .claude/skills/kosif-superpowers/scripts/skill_loader.py need "<task>" [-n 6] [--json]
  python3 .claude/skills/kosif-superpowers/scripts/skill_loader.py full           # full-power mode: what to open, in order

Python stdlib only. Read-only except `build`, which writes LOADER.md next to SKILL.md.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
SKILLS_ROOT = SKILL.parent
REPO = SKILLS_ROOT.parent.parent
OUT = SKILL / "LOADER.md"
HUBS_INDEX = SKILL / "data" / "hubs_index.json"
PROTOCOL = SKILL / "PROTOCOL.md"

FULL_MODE_TRIGGERS = ("فعّل كل القدرات", "فعل كل القدرات", "الوضع الكامل", "كل القدرات", "full power", "full mode",
                      "all capabilities", "activate everything")

FULL_MODE_LINE = ("**وضع التفعيل الكامل / Full-power mode:** لما المستخدم يقول «فعّل كل القدرات» أو «الوضع الكامل» "
                  "أو \"full power\"، شغّل كل القدرات والمهارات المناسبة بكامل عمقها: مستوى L3، كل الملاحق التي "
                  "يتحقق محفّزها، المجلس ومحامي الشيطان، النماذج الذهنية، ووكلاء متوازيين حيث توجد أداة Agent. "
                  "القوانين لا تتغير: لا تدّعِ تشغيل ما لم تشغّله، ولا دفع أو تثبيت نظامي أو مفاتيح أو نشر بلا إذن.")

STOP = set("the a an and or of to in for on with is are be this that من في على عن إلى الى و أو ثم مع هذا هذه ده دي".split())


def words(text: str) -> set[str]:
    return {w for w in re.findall(r"[\w؀-ۿ]{2,}", text.lower()) if w not in STOP}


def frontmatter(md: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", md, re.S)
    out = {}
    if m:
        for line in m.group(1).splitlines():
            k, sep, v = line.partition(":")
            if sep and not line.startswith(" "):
                out[k.strip()] = v.strip().strip('"')
    return out


def short(text: str, n: int = 170) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= n else text[: n - 1].rsplit(" ", 1)[0] + "…"


def sections(path: Path) -> list[dict]:
    """Level-1/2 headings of a Markdown file with their line ranges (1-based, inclusive)."""
    lines = path.read_text(encoding="utf-8").splitlines()
    heads, fence = [], False
    for i, line in enumerate(lines, 1):
        if line.startswith("```"):
            fence = not fence
        elif not fence and re.match(r"^#{1,2} ", line):
            heads.append((i, line.lstrip("#").strip()))
    out = []
    for k, (start, title) in enumerate(heads):
        end = heads[k + 1][0] - 1 if k + 1 < len(heads) else len(lines)
        out.append({"title": title, "start": start, "end": end})
    return out


def skills() -> list[dict]:
    out = []
    for f in sorted(SKILLS_ROOT.glob("*/SKILL.md")):
        md = f.read_text(encoding="utf-8")
        fm = frontmatter(md)
        out.append({"name": fm.get("name", f.parent.name), "path": f.relative_to(REPO).as_posix(),
                    "kb": round(len(md.encode("utf-8")) / 1024), "lines": md.count("\n") + 1,
                    "description": fm.get("description", ""), "sections": sections(f)})
    return out


def hubs() -> list[dict]:
    if not HUBS_INDEX.is_file():
        return []
    data = json.loads(HUBS_INDEX.read_text(encoding="utf-8"))
    return [{"id": h["id"], "ar": h.get("ar", ""), "en": h.get("en", ""), "start": h.get("start", ""),
             "keywords": h.get("keywords", [])} for h in data.get("hubs", [])]


def appendices() -> list[dict]:
    if not PROTOCOL.is_file():
        return []
    out = []
    for line in PROTOCOL.read_text(encoding="utf-8").splitlines():
        # one table row may name several appendices in its first cell: "[A43 …](…) · [A46 …](…) | trigger |"
        m = re.match(r"^\| ((?:\[A\d+[^\]]*\]\([^)]+\)(?: · )?)+) \| ([^|]+)\|", line)
        if not m:
            continue
        for title, path in re.findall(r"\[(A\d+[^\]]*)\]\(([^)]+)\)", m.group(1)):
            out.append({"id": re.match(r"A\d+", title).group(0), "title": title,
                        "path": f"{SKILL.relative_to(REPO).as_posix()}/{path}", "trigger": m.group(2).strip()})
    return out



def superskills() -> list[dict]:
    """Standalone 114-skill catalogue (files vendored under vendor/100-superskills)."""
    path = SKILL / "data" / "100-superskills-index.json"
    if not path.is_file():
        return []
    try:
        return json.loads(path.read_text(encoding="utf-8")).get("skills", [])
    except (ValueError, OSError):
        return []


def render() -> str:
    sk, hb, ap = skills(), hubs(), appendices()
    rel = SKILL.relative_to(REPO).as_posix()
    L = ["# LOADER — خريطة التحميل الخفيف / light loading map", "",
         "<!-- generated by scripts/skill_loader.py build; do not edit by hand -->", "",
         FULL_MODE_LINE, "",
         "## الفهرس / contents", "",
         "- المهارات / skills · المجموعات / groups · ملاحق البروتوكول / appendices · أقسام كل SKILL.md / section line ranges", "",
         "**التحميل الخفيف:** اقرأ هذا الملف وحده أولًا. لا تقرأ ملفات المهارات الكبيرة كاملة؛ افتح الملف أو "
         "نطاق الأسطر الذي يطابق الطلب فقط (`sed -n START,ENDp <path>`)، أو اسأل السكربت: "
         f"`python3 {rel}/scripts/skill_loader.py need \"<الطلب>\"`. كل مهارة وكل ملحق ممثَّل هنا بسطر، "
         "فلا توجد مهارة خارج الوصول. في الوضع الكامل: "
         f"`python3 {rel}/scripts/skill_loader.py full`.", "",
         f"## المهارات ({len(sk)}) / skills", "",
         "| المهارة | الملف | الحجم | متى |", "|---|---|---|---|"]
    for s in sk:
        L.append(f"| `{s['name']}` | `{s['path']}` | {s['kb']} KB · {s['lines']} سطر | {short(s['description']).replace('|', '/')} |")
    L += ["", f"## المجموعات ({len(hb)}) / capability groups", "", "| المجموعة | تغطي | أول أمر |", "|---|---|---|"]
    for h in hb:
        L.append(f"| `{h['id']}` | {h['ar']} — {h['en']} | `{h['start']}` |")
    L += ["", f"## ملاحق البروتوكول ({len(ap)}) / protocol appendices", "", "| الملحق | افتحه عندما |", "|---|---|"]
    for a in ap:
        L.append(f"| [{a['title']}]({Path(a['path']).relative_to(rel).as_posix()}) | {short(a['trigger'], 200)} |")
    L += ["", "## أقسام كل SKILL.md بأرقام الأسطر / section line ranges", ""]
    for s in sk:
        L += [f"### `{s['path']}`", ""]
        for sec in s["sections"]:
            L.append(f"- {sec['start']}–{sec['end']}: {short(sec['title'], 110)}")
        L.append("")
    L += ["", f"## مكتبة 100 Super Skills ({len(superskills())}) / vendored skills", "",
          "| المهارة | الفئة | SKILL.md |", "|---|---|---|"]
    for item in superskills():
        L.append(f"| `{item['slug']}` | `{item['category']}` | `{item['path']}` |")
    return "\n".join(L).rstrip() + "\n"


def need(task: str, n: int = 6) -> list[dict]:
    q = words(task)
    picks = []
    for h in hubs():
        score = len(q & words(" ".join(h["keywords"]) + " " + h["en"] + " " + h["ar"]))
        if score:
            picks.append({"kind": "group", "id": h["id"], "open": h["start"], "score": score})
    for a in appendices():
        score = len(q & words(a["trigger"] + " " + a["title"] + " " + Path(a["path"]).stem.replace("-", " ")))
        if score:
            picks.append({"kind": "appendix", "id": a["id"], "open": a["path"], "score": score})
    for s in skills():
        if s["name"] != "kosif-superpowers":
            score = len(q & words(s["description"]))
            if score:
                picks.append({"kind": "skill", "id": s["name"], "open": s["path"], "score": score})
        for sec in s["sections"]:
            score = len(q & words(sec["title"]))
            if score:
                picks.append({"kind": "section", "id": short(sec["title"], 60), "score": score,
                              "open": f"sed -n {sec['start']},{sec['end']}p {s['path']}"})
    for entry in superskills():
        score = len(q & words(entry["slug"].replace("-", " ") + " " + entry["ar"] + " " + entry["en"] + " " + entry["description"]))
        if score:
            picks.append({"kind": "superskill", "id": entry["slug"], "open": entry["path"],
                          "score": score, "note": "vendored: read vendor/100-superskills/skills/<slug>/SKILL.md"})
    picks.sort(key=lambda p: (-p["score"], p["kind"], p["id"]))
    return picks[:n]


def full_order() -> list[str]:
    rel = SKILL.relative_to(REPO).as_posix()
    return [f"{rel}/LOADER.md (this map)", f"{rel}/PROTOCOL.md (the core, in full)",
            f"python3 {rel}/scripts/boot.py && python3 {rel}/scripts/hub.py doctor",
            f"python3 {rel}/scripts/skill_intelligence.py brief \"<task>\" (100% inventory receipt)",
            "every appendix whose trigger matches (skill_loader.py need lists them)",
            f"python3 {rel}/scripts/think.py pro \"<task>\" --depth max (passes, models, council)",
            f"python3 {rel}/scripts/council.py plan \"<task>\" --dir out/<work>/council (members as parallel agents)",
            "the other skills under .claude/skills/ that match, each through its own SKILL.md"]


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--check", action="store_true")
    nd = sub.add_parser("need")
    nd.add_argument("task")
    nd.add_argument("-n", type=int, default=6)
    nd.add_argument("--json", action="store_true")
    sub.add_parser("full")
    a = p.parse_args(argv)
    if a.cmd == "build":
        text = render()
        if a.check:
            if not OUT.is_file() or OUT.read_text(encoding="utf-8") != text:
                print("LOADER.md is stale — run python3 scripts/skill_loader.py build", file=sys.stderr)
                return 1
            print("LOADER.md is current")
            return 0
        OUT.write_text(text, encoding="utf-8")
        print(f"wrote {OUT.relative_to(REPO)} ({len(text.splitlines())} lines)")
        return 0
    if a.cmd == "need":
        picks = need(a.task, a.n)
        if a.json:
            print(json.dumps(picks, ensure_ascii=False, indent=1))
        elif not picks:
            print("no match — open LOADER.md and pick by hand")
        else:
            for x in picks:
                print(f"[{x['kind']}] {x['id']}: {x['open']}")
        return 0
    print(FULL_MODE_LINE)
    for i, step in enumerate(full_order(), 1):
        print(f"{i}. {step}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
