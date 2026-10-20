#!/usr/bin/env python3
"""Boot: the first command of any session that uses this skill — Claude's self-briefing.

    python3 scripts/boot.py                    # live briefing: machine, counts, what is ready NOW, top installs to unlock more, how to think
    python3 scripts/boot.py --json             # the same as JSON
    python3 scripts/boot.py --static --write   # regenerate CAPABILITIES.md and llms.txt at the repo root (for a bare repository link)
    python3 scripts/boot.py --static --check   # exit 1 if those files are stale

Read-only and stdlib only (~2 s). "Ready now" means every requirement of the power is detected on this machine;
it is presence, not proof — ✅ still needs a real run.
"""
from __future__ import annotations

import argparse
import json
import platform
import shutil
import signal
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
REPO = SKILL.parents[2] if SKILL.parent.name == "skills" else SKILL
RAW = "https://raw.githubusercontent.com/kosif199022-jpg/kosif-tool/main/"
GH = "https://github.com/kosif199022-jpg/kosif-tool/blob/main/"
SK_REL = ".claude/skills/kosif-superpowers/"
DOM_AR = {"mind": "العقل والتفكير", "craft": "الكتابة واللغة", "code": "الهندسة والكود", "data": "البيانات", "docs": "المستندات",
          "research": "البحث والويب", "build": "التطبيقات والواجهات", "media": "الصور والصوت", "strategy": "المنتج والمال", "motion": "الموشن والمونتاج"}


def load():
    sys.path.insert(0, str(HERE))
    import powers as P  # noqa: E402
    import requirements as R  # noqa: E402
    return P, R, P.load_powers(), R.registry()


def summary(P, pw):
    by_dom = defaultdict(list)
    for p in pw:
        by_dom[p.get("domain") or P.DEFAULT_DOMAIN].append(p)
    fams = defaultdict(list)
    for p in pw:
        fams[p["family"]].append(p)
    return by_dom, fams


def live(as_json: bool) -> int:
    P, R, pw, reg = load()
    pres = R.present(reg)
    by_dom, fams = summary(P, pw)
    ready = [p for p in pw if all(pres.get(k) == "present" for k in (p.get("requires") or []))]
    blocked = Counter(k for p in pw for k in (p.get("requires") or []) if pres.get(k) == "missing")
    unlock = []
    for k, n in blocked.most_common(12):
        unlock.append({"requirement": k, "unlocks": n, "install": reg[k].get("install", ""), "kind": reg[k].get("kind")})
    st = Counter(p.get("status") for p in pw)
    data = {
        "machine": {"os": platform.platform(), "python": platform.python_version(),
                    "node": bool(shutil.which("node")), "ffmpeg": bool(shutil.which("ffmpeg")), "gpu": bool(shutil.which("nvidia-smi"))},
        "catalog": {"powers": len(pw), "families": len(fams), "domains": len(by_dom), "status": dict(st)},
        "ready_now": len(ready),
        "by_domain": {d: {"powers": len(v), "proven": sum(p.get("status") == "proven" for p in v),
                          "ready_now": sum(1 for p in v if p in ready)} for d, v in sorted(by_dom.items(), key=lambda kv: -len(kv[1]))},
        "requirements": {s: sum(1 for v in pres.values() if v == s) for s in ("present", "missing", "unknown")},
        "top_unlocks": unlock,
    }
    if as_json:
        print(json.dumps(data, ensure_ascii=False, indent=1)); return 0
    m = data["machine"]
    print(f"# KOSIF Superpowers — boot ({m['os']}, python {m['python']}, node {'✓' if m['node'] else '✗'}, ffmpeg {'✓' if m['ffmpeg'] else '✗'}, GPU {'✓' if m['gpu'] else '✗'})\n")
    print(f"catalog: {len(pw):,} powers · {len(fams)} families · {len(by_dom)} domains · ✅ {st['proven']} proven · 🟢 {st['ready']} ready · 📦 {st['install']} install · 🔑 {st['key']} key")
    print(f"ready NOW on this machine (every requirement present): {len(ready):,} powers")
    print(f"requirements: 🟢 {data['requirements']['present']} present · 📦 {data['requirements']['missing']} missing · ❔ {data['requirements']['unknown']} unknown\n")
    print("domain              powers  proven  ready-now")
    for d, v in data["by_domain"].items():
        print(f"  {d:<10} {DOM_AR.get(d, ''):<18} {v['powers']:>6} {v['proven']:>7} {v['ready_now']:>10}")
    print("\nbiggest unlocks (one install each — ask before paid or system-wide installs):")
    for u in unlock[:8]:
        print(f"  +{u['unlocks']:<4} {u['requirement']:<20} → {u['install']}")
    print("""
structure: 20 hubs → 456 fused superpowers → every atomic power (START.md · references/hubs.md)
next:
  1. python3 scripts/kosif_hubs.py route "<task>"     hub + superpowers + scripts + install plan
  2. python3 scripts/kosif_hubs.py install <hub>      install what is missing (--apply: pip/npm only)
  3. python3 scripts/superpower_fusion.py show SP-…   the superpower's ordered members and links
  4. python3 scripts/think.py frame "<task>"          the contract, then build a thin slice and verify it
map: references/capability-graph.html · thinking: references/cognition.md · rules: SKILL.md §6""")
    return 0


# ------------------------------------------------------------------ static files for a bare repo link
def capabilities_md(P, R, pw, reg) -> str:
    by_dom, fams = summary(P, pw)
    st = Counter(p.get("status") for p in pw)
    L = ["# CAPABILITIES — ما يستطيعه Claude مع هذا المستودع / what Claude can do with this repository", "",
         "<!-- generated by .claude/skills/kosif-superpowers/scripts/boot.py --static --write; do not edit by hand -->", "",
         "> **إلى Claude:** إن أرسل لك المستخدم رابط هذا المستودع فهذه الصفحة هي خريطتك الذاتية. اقرأها كاملة، ثم حمّل المهارة وشغّل `boot.py` إن كان لديك shell. كل رقم هنا مولَّد من بيانات الكتالوج، وكل قدرة لها شارة دليل صادقة.",
         "> **To Claude:** if the user sends you this repository's link, this page is your self-model. Read it, then load the skill and run `boot.py` if you have a shell. Every number below is generated from the catalog data; every power carries an honest evidence badge.", "",
         "## الفهرس / contents",
         "1. [كيف تبدأ / how to start](#start)", "2. [الأرقام / numbers](#numbers)", "3. [المجالات والعائلات / domains and families](#domains)",
         "4. [المستلزمات الأكثر فتحًا / biggest unlocks](#unlocks)", "5. [طريقة التفكير / how to think](#think)", "6. [قواعد الصدق / honesty rules](#rules)", "7. [روابط مباشرة / raw links](#links)", "",
         "<a id=\"start\"></a>", "## 1. كيف تبدأ / how to start", "",
         "| أين أنت / surface | افعل / do |", "|---|---|",
         "| Claude Code (CLI, desktop, web) داخل المستودع | المهارة تُحمَّل تلقائيًا. نفّذ: `python3 .claude/skills/kosif-superpowers/scripts/boot.py` ثم اتبع خطواته الأربع. |",
         "| Claude Code مع رابط فقط | استنسخ المستودع (`git clone https://github.com/kosif199022-jpg/kosif-tool`) ثم كما أعلاه. |",
         "| claude.ai محادثة مع رابط فقط، بلا shell | اقرأ هذه الصفحة، ثم [SKILL.md](" + RAW + SK_REL + "SKILL.md) و[cognition.md](" + RAW + SK_REL + "references/cognition.md)، وافتح فصل العائلة المناسبة من الجدول أدناه. لا تدّعِ تشغيل شيء لم تشغّله. |",
         "| claude.ai مع تنفيذ كود | ارفع ملف zip للمهارة أو اقرأ الملفات الخام، ثم شغّل السكربتات القياسية (stdlib) داخل بيئة التنفيذ. |", "",
         "<a id=\"numbers\"></a>", "## 2. الأرقام / numbers", "",
         f"**{len(pw):,}** قدرة · **{len(fams)}** عائلة · **{len(by_dom)}** مجالات · ✅ {st['proven']} مُثبتة بتشغيل فعلي · 🟢 {st['ready']} جاهزة · 📦 {st['install']} بأمر تثبيت · 🔑 {st['key']} بمفتاح أو حساب · 👁 {st['seen']} شوهدت في فيديو مرجعي · 📄 {st['documented']} طريقة موصوفة · 💡 {st['idea']} فكرة.",
         f"المستلزمات المسجّلة: **{len(reg)}** (أدوات، حزم، مفاتيح، منصات، خطوط، نماذج)؛ النماذج الذهنية: **63**؛ خريطة الأدوات: **124** مستودعًا موثّق الترخيص.", "",
         "<a id=\"domains\"></a>", "## 3. المجالات والعائلات / domains and families", ""]
    for d, rows in sorted(by_dom.items(), key=lambda kv: -len(kv[1])):
        dst = Counter(p.get("status") for p in rows)
        L += [f"### {DOM_AR.get(d, d)} / {d} — {len(rows):,} powers · ✅ {dst['proven']}", "",
              "| family | prefix | powers | ✅ | examples (proven first) |", "|---|---|---|---|---|"]
        fs = defaultdict(list)
        for p in rows:
            fs[p["family"]].append(p)
        for fam, fr in sorted(fs.items(), key=lambda kv: -len(kv[1])):
            ttl = P.family_title(fam)
            name = f"{ttl[0]} — {ttl[1]}" if isinstance(ttl, tuple) else fam
            ex = sorted(fr, key=lambda r: (r.get("status") != "proven", r["id"]))[:3]
            exs = "; ".join(f"{r['id']} {r.get('name_en', '')[:46]}" for r in ex).replace("|", "/")
            L.append(f"| [{name}]({GH}{SK_REL}references/powers/{fam}.md) | {P.prefix_of(fr[0])} | {len(fr)} | {sum(r.get('status') == 'proven' for r in fr)} | {exs} |")
        L.append("")
    blocked = Counter(k for p in pw for k in (p.get("requires") or []))
    L += ["<a id=\"unlocks\"></a>", "## 4. المستلزمات الأكثر فتحًا / biggest unlocks", "",
          "كل سطر: مستلزم، كم قدرة تحتاجه، وأمر تثبيته. الفهرس الكامل: [requirements.md](" + GH + SK_REL + "references/requirements.md). — Each row: a requirement, how many powers need it, and its install command.", "",
          "| requirement | kind | powers | install |", "|---|---|---|---|"]
    for k, n in blocked.most_common(25):
        v = reg.get(k, {})
        L.append(f"| `{k}` | {v.get('kind', '')} | {n} | `{v.get('install', '').replace('|', '/')[:110]}` |")
    L += ["", "<a id=\"think\"></a>", "## 5. طريقة التفكير / how to think", "",
          "1. **العمق / depth:** `think.py ladder \"<task>\"` يختار مستوى التفكير L0–L6 وإجراءه.",
          "2. **العقد / contract:** `think.py frame \"<task>\"` — الهدف، القارئ، معايير الإنجاز، القيود، المجهولات، أول فحص.",
          "3. **القوى / powers:** `powers.py suggest \"<task>\"` ثم `requirements.py plan \"<task>\"` (▶ = يبدأ الآن).",
          "4. **النماذج الذهنية / models:** `think.py models \"<problem>\"` من 63 نموذجًا.",
          "5. **الأفكار / ideas:** `think.py ideas \"<seed>\" -n 12` ثم التقييم بالجدة × الجدوى.",
          "6. **القرار / decide:** `think.py decide decision.json` مع فحص الحساسية؛ `think.py fermi` للتقديرات.",
          "7. **التخطيط / plan:** `think.py plan \"<goal>\" --weeks N`.",
          "8. **التحقق / verify:** افتح الناتج نفسه، احسب الأرقام بالكود، `think.py critic draft.md` قبل الإرسال.",
          "", "الدليل الكامل: [cognition.md](" + GH + SK_REL + "references/cognition.md) — سلّم التفكير، عادات العباقرة، تطوير الأفكار، التخطيط، القرار، التفكير الشبيه بالبشر، المراقبة الذاتية.", "",
          "<a id=\"rules\"></a>", "## 6. قواعد الصدق / honesty rules", "",
          "- أدنى شارة صادقة دائمًا. ✅ يعني تشغيلًا فعليًا بدليل؛ وجود رابط أو حزمة ليس قدرة. — Always the lowest true badge.",
          "- `proof_scope` يقول أين الدليل: `repo` قابل للفحص هنا، `sibling` في مستودع آخر للمالك. — Know where the evidence lives.",
          "- لا «لا أستطيع» قبل الفحص: خريطة → فحص → تثبيت → بديل. — Registry before no.",
          "- لا تثبيت مدفوع أو شامل للنظام، ولا مفاتيح، ولا نشر بلا موافقة. — Consent for paid, system-wide or outward actions.",
          "- لا نسخ لكود أو وسائط أو برومبتات طرف ثالث بلا ترخيص؛ اربط وانسب. — Link and credit.",
          "- صوت المستخدم لا يُمس، والفحص القانوني فقط لما يملك المستخدم حق فحصه. — User audio untouched; lawful inspection only.", "",
          "<a id=\"links\"></a>", "## 7. روابط مباشرة / raw links", ""]
    for name, path in [("SKILL.md", "SKILL.md"), ("cognition.md", "references/cognition.md"), ("requirements.md", "references/requirements.md"),
                       ("capability-map.md", "references/capability-map.md"), ("capability-graph.html", "references/capability-graph.html"),
                       ("repos.md (124 tools)", "references/repos.md"), ("mental_models.json", "data/mental_models.json"),
                       ("requirements.json", "data/requirements.json"), ("capability_graph.json", "data/capability_graph.json")]:
        L.append(f"- {name}: {RAW}{SK_REL}{path}")
    L.append("")
    return "\n".join(L)


def llms_txt(P, pw) -> str:
    st = Counter(p.get("status") for p in pw)
    fams = sorted({p["family"] for p in pw})
    L = ["# KOSIF TOOL — Claude superpowers and Arabic-first motion-graphics atlas", "",
         f"> A Claude Code skill that tells Claude what it can really do: {len(pw):,} powers in {len(fams)} families and 10 domains, each with an evidence badge "
         f"({st['proven']} proven by real runs), the requirements to run it, executable thinking tools, and a 288-style motion-graphics atlas.", "",
         "Start with CAPABILITIES.md, then the skill's SKILL.md. Inside Claude Code run `python3 .claude/skills/kosif-superpowers/scripts/boot.py`.", "",
         "## Start", f"- [CAPABILITIES.md]({RAW}CAPABILITIES.md): generated self-model for Claude",
         f"- [SKILL.md]({RAW}{SK_REL}SKILL.md): the skill and its power-up protocol",
         f"- [cognition.md]({RAW}{SK_REL}references/cognition.md): how to think, plan, decide and create",
         f"- [requirements.md]({RAW}{SK_REL}references/requirements.md): what each power needs and what each install unlocks", "",
         "## Families"]
    for f in fams:
        L.append(f"- [{f}]({RAW}{SK_REL}references/powers/{f}.md)")
    L += ["", "## Optional", f"- [repos.md]({RAW}{SK_REL}references/repos.md): 124 credited open-source tools",
          f"- [AGENTS.md]({RAW}AGENTS.md): motion-graphics production rules", f"- [STYLE_INDEX.md]({RAW}STYLE_INDEX.md): 288 styles", ""]
    return "\n".join(L)


def static(write: bool, check: bool) -> int:
    P, R, pw, reg = load()
    files = {REPO / "CAPABILITIES.md": capabilities_md(P, R, pw, reg), REPO / "llms.txt": llms_txt(P, pw)}
    stale = [p for p, t in files.items() if not p.exists() or p.read_text(encoding="utf-8") != t]
    if check:
        for p in stale:
            print(f"stale: {p.name} — run python3 {SK_REL}scripts/boot.py --static --write")
        return 1 if stale else 0
    if write:
        for p, t in files.items():
            p.write_text(t, encoding="utf-8")
            print(f"wrote {p.relative_to(REPO)} ({len(t):,} chars)")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true"); ap.add_argument("--static", action="store_true")
    ap.add_argument("--write", action="store_true"); ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    return static(a.write, a.check) if a.static else live(a.json)


if __name__ == "__main__":
    if hasattr(signal, "SIGPIPE"):
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    sys.exit(main())
