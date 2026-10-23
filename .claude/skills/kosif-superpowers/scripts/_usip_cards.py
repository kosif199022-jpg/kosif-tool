"""USIP v5.5 full protocol library: one protocol card per catalog power and per runnable tool.

Used by `smart_capabilities.py cards|cards-check`. Every card applies the rules of appendices A25-A29
(data/usip_intelligence.json) to one record of data/powers/*.json or data/tools.json, so the library is
regenerable and deterministic: edit the catalog or the rules, never the generated files.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
REPO = BASE.parent.parent.parent
POWERS = BASE / "data" / "powers"
TOOLS = BASE / "data" / "tools.json"
INTEL = BASE / "data" / "usip_intelligence.json"
MODES = BASE / "data" / "reasoning_modes.json"
MODELS = BASE / "data" / "mental_models.json"
OUT = REPO / "usip-library"
SK_REL = "../../../.claude/skills/kosif-superpowers"   # from usip-library/cards/<group>/ to the skill folder
RAW = "https://raw.githubusercontent.com/kosif199022-jpg/kosif-tool/main/usip-library/"

# group -> deliverable kind of data/usip_intelligence.json; a family override wins
GROUP_KIND = {"research": "research", "thinking": "plan", "agents": "plan", "software": "code", "drawing": "image",
              "images": "image", "3d": "model3d", "motion": "video", "audio": "audio", "type": "image", "data": "data",
              "documents": "document", "quality": "code", "reverse": "code", "misc": "plan"}
FAMILY_KIND = {"strategy-finance": "finance", "atlas-docs": "document", "writing-humanizer": "document",
               "documents-office": "document", "arabic-language": "translation", "voice-tts": "audio",
               "audio-sync-captions": "audio", "music-beat-sound": "audio", "charts-data-infographic": "data",
               "prompt-craft": "document", "web-research": "research", "atlas-research": "research"}
# FusionForge artifact kinds for the typed node of each deliverable kind
NODE_KIND = {"video": ("audio", "video"), "audio": ("audio", "dataset"), "image": ("spec", "image"), "code": ("spec", "code"),
             "data": ("dataset", "report"), "research": ("brief", "report"), "document": ("brief", "document"),
             "translation": ("document", "document"), "slides": ("document", "document"), "model3d": ("spec", "model3d"),
             "finance": ("dataset", "report"), "plan": ("brief", "plan")}
STAGES = {
    "video": "قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم",
    "audio": "قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم",
    "image": "المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG",
    "code": "قراءة الكود والاختبارات ← إعادة إنتاج أو اختبار جديد ← أصغر تغيير ← الاختبارات ← مراجعة الفرق ← فرع وPR",
    "data": "فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت",
    "research": "السؤال والنطاق ← مصادر بتواريخها ← حقائق بمراجعها ← تركيب ورأي مخالف ← تدقيق ادعاء ← دليل ← تسليم",
    "document": "الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم",
    "translation": "المصطلحات الثابتة ← ترجمة ← مقابلة جملة بجملة ← مطابقة الأرقام والأسماء ← قراءة طبيعية ← تسليم",
    "slides": "الجمهور والهدف ← عناوين تحكي القصة ← شريحة لكل فكرة ← مصادر الأرقام ← تسليم",
    "model3d": "المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل",
    "finance": "المدخلات والمعيار ← حساب حتمي بالأعداد الصحيحة ← تسوية ← مراجعة المعالجة بمعيارها ← تسليم",
    "plan": "الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع",
}
SEVERITY = {"assume": "افتراض مكتوب", "ask": "سؤال بإجابة مقترحة", "blocker": "مدخل حاجب"}
STATUS = {
    "proven": ("✅", "مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة", "V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك"),
    "ready": ("🟢", "جاهزة حسب الكتالوج بلا إعداد", "V2 بعد تشغيلها، وV3 بعد قياس معيار"),
    "documented": ("📄", "منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل", "V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا"),
    "seen": ("👁", "شوهدت في مرجع أو عرض ولم تُنفّذ هنا", "V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط"),
    "install": ("📦", "تحتاج حزمة أو برنامجًا أو نموذجًا أولًا", "V1 حتى تُثبَّت (التثبيت النظامي بإذن)"),
    "key": ("🔑", "تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة", "لا استدعاء قبل إذن صريح ومعرفة التكلفة"),
    "idea": ("💡", "فكرة غير مبنية", "V0؛ تُعرض فكرةً لا قدرة"),
}
REQ_CHECK = (("pip:", "python3 -c \"import {m}\" (اسم الاستيراد قد يختلف عن اسم الحزمة)"), ("npm:", "npm ls {m} أو وجود node_modules/{m}"),
             ("bin:", "{m} --version أو which {m}"), ("key:", "حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف"),
             ("model:", "النموذج المحلي موجود في مجلد النماذج قبل التشغيل"), ("font:", "ملف الخط ورخصته من مصدره"),
             ("net:", "الشبكة مسموحة في هذه الجلسة"), ("app:", "التطبيق مثبت ويُفتح بإذن"))


def _c(v) -> str:
    return re.sub(r"\s+", " ", str(v or "")).strip().replace("|", "\\|").replace("](", "]\\(")   # record text never becomes a link


def _slug(title: str) -> str:
    import unicodedata
    t = re.sub(r"`|\*\*|__", "", title.strip()).lower()
    return "".join(c for c in t if c in " -_" or unicodedata.category(c)[0] in "LMN").replace(" ", "-")


def load():
    import smart_capabilities as sc   # the group spec is the single source of the family -> group map
    groups, fam_group = {}, {}
    for slug, ar, en, csv, _keys in sc.SPEC:
        groups[slug] = {"id": slug, "ar": ar, "en": en}
        for f in csv.split(","):
            fam_group[f.strip()] = slug
    records = []
    for f in sorted(POWERS.glob("*.json")):
        records += json.loads(f.read_text(encoding="utf-8-sig"))
    reg = json.loads(TOOLS.read_text(encoding="utf-8"))
    intel = json.loads(INTEL.read_text(encoding="utf-8"))
    return groups, fam_group, records, reg, intel


def kind_of(family: str, group: str) -> str:
    return FAMILY_KIND.get(family) or GROUP_KIND.get(group, "plan")


def req_line(r: str) -> str:
    for pre, tpl in REQ_CHECK:
        if r.startswith(pre):
            return f"- `{_c(r)}` ← " + tpl.format(m=_c(r[len(pre):]))
    return f"- `{_c(r)}` ← افحص وجوده بأمر واحد قبل كتابة الشارة"


def recovery_lines(rec: dict, intel: dict, kind: str, family_tools: list) -> list:
    classes = []
    if rec.get("requires") or rec.get("install"):
        classes.append("missing_dependency")
    if kind in ("video", "audio", "image", "model3d", "data", "translation"):
        classes.append("wrong_input_kind")
    classes.append("quality_below_threshold")
    if family_tools:
        classes.append("tool_error")
    if any(str(r).startswith("key:") for r in rec.get("requires", [])):
        classes.append("permission_denied")
    if kind in ("video", "audio", "image") and not rec.get("license"):
        classes.append("license_blocked")
    out = []
    for c in classes:
        r = intel["recovery"][c]
        out.append(f"- `{c}` ({r['ar']}، ميزانية {r['budget']}): {r['diagnose'][0]} ← {r['fix'][0]} · البديل: {r['fallback']} · تصعيد: {r['escalate']}")
    return out


def card_title(rec) -> str:
    return f"`{rec['id']}` — {_c(rec['name_ar'])} / {_c(rec['name_en'])}"


def power_card(rec, groups, fam_group, intel, family_tools, siblings) -> list:
    fam = rec["family"]
    group = fam_group.get(fam, "misc")
    kind = kind_of(fam, group)
    k = intel["kinds"][kind]
    badge, meaning, ceiling = STATUS.get(rec["status"], ("?", rec["status"], "—"))
    nin, nout = NODE_KIND[kind]
    L = [f"### {card_title(rec)}", "",
         "| الحقل | القيمة |", "|---|---|",
         f"| العائلة | `{fam}` ([فصل العائلة]({SK_REL}/references/powers/{fam}.md)) |",
         f"| المجموعة | {groups[group]['ar']} (`{group}`) |",
         f"| نوع المخرج (A25، A27) | {k['ar']} (`{kind}`) |",
         f"| الحالة في الكتالوج | {badge} `{rec['status']}`: {meaning} |",
         f"| سقف التحقق قبل العمل (A27) | {ceiling} |",
         f"| نطاق الدليل | `{_c(rec.get('proof_scope')) or 'none'}` |",
         f"| الرخصة | {_c(rec.get('license')) or 'غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم'} |", "",
         f"**ما هي:** {_c(rec.get('what')) or '—'}", "",
         f"**متى:** {_c(rec.get('when')) or '—'}", "",
         f"**كيف:** {_c(rec.get('how')) or '—'}", ""]
    if _c(rec.get("params")):
        L += [f"**المعاملات:** {_c(rec['params'])}", ""]
    L += [f"**التثبيت:** {_c(rec.get('install')) or 'لا خطوة تثبيت مسجلة'}", "",
          f"**الوسوم:** {' · '.join(_c(t) for t in rec.get('tags', [])) or '—'}", "",
          "#### 1. الاستقبال (A25)", ""]
    L += [f"- {s['ar']}: {SEVERITY[s['severity']]} ← {s['default']}" for s in k["slots"]]
    L += ["- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.", "",
          "#### 2. الجاهزية والشارة (A28)", ""]
    reqs = rec.get("requires", [])
    L += [req_line(r) for r in reqs] if reqs else ["- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة."]
    L += [f"- الوضع 1: شارة «هنا الآن» بعد الفحص، لا {badge} الكتالوج تلقائيًا · الوضع 2: `كتالوج: {badge} · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.", "",
          "#### 3. موضعها في الخطة (A26)", "",
          f"- عقدة منمّطة: المدخل `{nin}` ← المخرج `{nout}`، والمنفّذ `method:{rec['id']}` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).",
          ("- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): " + " · ".join(f"`{t}`" for t in family_tools[:6]) + "."
           if family_tools else "- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى."),
          f"- مراحل النوع: {STAGES[kind]}.",
          "- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.", "",
          "#### 4. بوابة التحقق (A27)", ""]
    L += [f"- {'إلزامي' if q['hard'] else 'جودة'}: {q['ar']} ← {q['tool']}" for q in k["quality"]]
    L += [f"- أمر الحكم في الوضع 1: `think.py qa {kind} --answers qa.json` (PASS / FAIL / INCOMPLETE).", "",
          "#### 5. التعافي (A29)", ""]
    L += recovery_lines(rec, intel, kind, family_tools)
    L += ["", "#### 6. الأدلة", ""]
    L += [f"- `{_c(p)}`" for p in rec.get("proof", [])] or ["- لا دليل مسجل: لا تُقدَّم أكثر من منهج."]
    L += ["", "#### 7. قدرات قريبة في العائلة", ""]
    L += [f"- `{s['id']}` {_c(s['name_ar'])} / {_c(s['name_en'])} ({s['status']})" for s in siblings] or ["- لا شيء."]
    return L + [""]


def tool_card(t, intel) -> list:
    L = [f"### `{t['id']}` — {_c(t.get('title_ar'))} / {_c(t.get('title_en'))}", "",
         "| الحقل | القيمة |", "|---|---|",
         f"| المسار | `{_c(t.get('path'))}` (جذر: {t.get('root')}) |", f"| المجال | `{t.get('area')}` |",
         f"| الدليل | `{_c(t.get('evidence'))}` |", f"| العائلات | {', '.join(f'`{f}`' for f in t.get('families', []))} |", "",
         f"**ما تفعله:** {_c(t.get('summary_ar'))}", "", f"**What it does:** {_c(t.get('summary_en'))}", "",
         "#### متى تُستدعى", ""]
    L += [f"- «{_c(u)}»" for u in t.get("use_when", [])]
    L += ["", "#### الأوامر", ""]
    for c in t.get("commands", []):
        L += [f"- **{_c(c.get('name'))}**: {_c(c.get('does'))}", f"  - `{_c(c.get('example'))}`"]
    L += ["", "#### المتطلبات والأمان", ""]
    req = t.get("requires") or {}
    if isinstance(req, dict):
        for kk, vv in sorted(req.items()):
            if vv:
                L.append(f"- {kk}: {_c(vv if isinstance(vv, str) else ', '.join(map(str, vv)) if isinstance(vv, list) else json.dumps(vv, ensure_ascii=False))}")
    elif req:
        L.append(f"- {_c(', '.join(map(str, req)))}")
    L += [f"- الأمان: {_c(t.get('safety')) or '—'}", f"- الموافقة: {_c(t.get('consent')) or '—'}", f"- الحدود: {_c(t.get('limits')) or '—'}"]
    L += ["", "#### الاختبارات والأدلة", ""]
    L += [f"- `{_c(x)}`" for x in t.get("tests", [])] or ["- لا اختبار مسجل: الشارة لا تتجاوز 📄 حتى يُختبر هنا."]
    L += [f"- مرجع: `{_c(d)}`" for d in t.get("docs", [])]
    L += ["", "#### عند الفشل (A29)", "",
          f"- ابدأ بـ `think.py recover --message \"<نص الخطأ>\"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action \"<ما جُرّب>\" --result failed --error-class <الصنف> --tool tool:{t['id']} --evidence <ملف>`.", ""]
    return L


def methods_pages(intel) -> dict:
    pages = {}
    modes = json.loads(MODES.read_text(encoding="utf-8"))["modes"]
    L = ["# أنماط الاستدلال / reasoning modes", "", "> مولّد من `data/reasoning_modes.json` (الملحق A24). [الفهرس](../README.md)", ""]
    for m in modes:
        L += [f"## {m['ar']} / {m['en']} (`{m['id']}`)", "", f"**متى:** {_c(m['use_when'])}", "", "**الخطوات:**", ""]
        L += [f"{i}. {_c(s)}" for i, s in enumerate(m["procedure"], 1)]
        L += ["", f"**الفخ:** {_c(m['trap'])}", "", f"**الفحص:** {_c(m['check'])}", ""]
    pages["methods/reasoning-modes.md"] = L
    try:
        raw = json.loads(MODELS.read_text(encoding="utf-8"))
        models = raw.get("models", raw) if isinstance(raw, dict) else raw
    except (OSError, ValueError):
        models = []
    L = ["# النماذج الذهنية / mental models", "", "> مولّد من `data/mental_models.json`. [الفهرس](../README.md)", ""]
    for m in models if isinstance(models, list) else []:
        title = " / ".join(x for x in (m.get("name_ar"), m.get("name_en")) if x) or m.get("id")
        L += [f"## {_c(title)} (`{_c(m.get('id'))}`)", ""]
        for key, val in m.items():
            if key in ("id", "name_ar", "name_en"):
                continue
            if isinstance(val, list):
                L += [f"**{key}:**", ""] + [f"- {_c(v)}" for v in val] + [""]
            elif val:
                L += [f"**{key}:** {_c(val)}", ""]
    pages["methods/mental-models.md"] = L
    L = ["# معايير الجودة وسلالم التعافي / quality bars and recovery ladders", "",
         "> مولّد من `data/usip_intelligence.json` (الملاحق A25 وA27 وA29). [الفهرس](../README.md)", ""]
    for kid, k in intel["kinds"].items():
        L += [f"## {k['ar']} (`{kid}`)", "", "**خانات الاستقبال:**", ""]
        L += [f"- {s['ar']}: {SEVERITY[s['severity']]} ← {s['default']}" for s in k["slots"]]
        L += ["", "**معايير الجودة:**", ""] + [f"- {'إلزامي' if q['hard'] else 'جودة'}: {q['ar']} ← {q['tool']}" for q in k["quality"]]
        L += ["", f"**المراحل:** {STAGES[kid]}", ""]
    for c, r in intel["recovery"].items():
        L += [f"## التعافي: {r['ar']} (`{c}`)", "", f"الميزانية: {r['budget']} · العلامات: {', '.join(r['signals'])}", "", "**التشخيص:**", ""]
        L += [f"{i}. {s}" for i, s in enumerate(r["diagnose"], 1)] + ["", "**الإصلاح:**", ""]
        L += [f"{i}. {s}" for i, s in enumerate(r["fix"], 1)] + ["", f"**البديل:** {r['fallback']}", "", f"**التصعيد:** {r['escalate']}", ""]
    L += ["## سلم التحقق / verification ladder", ""] + [f"- {v['id']}: {v['ar']} ← `{v['status']}`" for v in intel["verification_ladder"]] + [""]
    pages["methods/quality-and-recovery.md"] = L
    return pages


def build() -> dict:
    """{relative path: text} for usip-library/. Deterministic."""
    groups, fam_group, records, reg, intel = load()
    by_family = {}
    for r in records:
        by_family.setdefault(r["family"], []).append(r)
    fam_tools = {}
    for t in reg["tools"]:
        for f in t.get("families", []):
            fam_tools.setdefault(f, []).append(t["id"])
    pages, index_rows = {}, []
    for fam in sorted(by_family):
        recs = sorted(by_family[fam], key=lambda r: r["id"])
        group = fam_group.get(fam, "misc")
        ev = {t["id"]: t.get("evidence") for t in reg["tools"]}
        tools = sorted(set(fam_tools.get(fam, [])), key=lambda i: (ev.get(i) != "tested-here", i))   # tested here first
        L = [f"# `{fam}` — {groups[group]['ar']} ({len(recs):,} بطاقة)", "",
             f"> مكتبة بروتوكول USIP v5.5 الكاملة، مولّدة بـ `smart_capabilities.py cards` من `data/powers/{fam}.json` وقواعد الملاحق A25–A29؛ لا تُحرَّر يدويًا. "
             f"[الفهرس الرئيسي](../../README.md) · [فصل المجموعة]({SK_REL}/references/library/{group}.md) · [النواة]({SK_REL}/PROTOCOL.md)", "",
             "## الفهرس / contents", ""]
        L += [f"- [`{r['id']}` {_c(r['name_ar'])}](#{_slug(card_title(r))})" for r in recs]
        L += ["", "## البطاقات / cards", ""]
        for i, r in enumerate(recs):
            sib = [s for s in recs[max(0, i - 2):i + 3] if s["id"] != r["id"]][:4]
            L += power_card(r, groups, fam_group, intel, tools, sib)
        path = f"cards/{group}/{fam}.md"
        pages[path] = L
        index_rows.append((group, fam, len(recs), len(L), path))
    by_area = {}
    for t in reg["tools"]:
        by_area.setdefault(t.get("area", "other"), []).append(t)
    tool_rows = []
    for area in sorted(by_area):
        ts = sorted(by_area[area], key=lambda t: t["id"])
        L = [f"# أدوات المجال `{area}` ({len(ts)} أداة)", "",
             "> مولّد من `data/tools.json`. [الفهرس الرئيسي](../README.md) · `python3 scripts/hub.py tool <id>` للبطاقة الحية.", ""]
        for t in ts:
            L += tool_card(t, intel)
        pages[f"tools/{area}.md"] = L
        tool_rows.append((area, len(ts), len(L), f"tools/{area}.md"))
    pages.update(methods_pages(intel))
    total = sum(len(v) + 1 for v in pages.values())
    I = ["# مكتبة بروتوكول USIP v5.5 الكاملة / the full USIP v5.5 protocol library", "",
         f"> مولّدة بـ `python3 .claude/skills/kosif-superpowers/scripts/smart_capabilities.py cards` من كتالوج KOSIF وقواعد الملاحق A25–A29؛ لا تُحرَّر يدويًا، وتُفحص بـ `cards-check`. "
         f"النواة المحمولة للصق: [USIP_PORTABLE.md]({SK_REL[6:]}/USIP_PORTABLE.md).", "",
         "## الفهرس / contents", "", "- [ما هذه المكتبة](#ما-هذه-المكتبة)", "- [بطاقات القدرات](#بطاقات-القدرات)",
         "- [بطاقات الأدوات](#بطاقات-الأدوات)", "- [المناهج](#المناهج)", "- [الروابط الخام](#الروابط-الخام)", "",
         "## ما هذه المكتبة", "",
         f"بطاقة بروتوكول لكل قدرة في الكتالوج ({len(records):,}) ولكل أداة قابلة للتشغيل ({len(reg['tools'])})، في {len(pages) + 1} ملفًا و{total:,} سطرًا تقريبًا مع هذا الفهرس. "
         "كل بطاقة تجمع سجل القدرة نفسه (ما هي، متى، كيف، التثبيت، المتطلبات، الأدلة، الرخصة) مع قواعد البروتوكول مطبّقة عليها: خانات الاستقبال (A25)، والجاهزية والشارة الصادقة (A28)، "
         "وموضعها عقدةً منمّطة في الخطة (A26)، وبوابة التحقق لنوع مخرجها (A27)، وسلم التعافي لأخطائها المرجحة (A29). القواعد العامة تتكرر عمدًا في كل بطاقة لتُقرأ البطاقة وحدها؛ "
         "والمعرفة الفريدة في سجلات الكتالوج والملاحق. حالة الكتالوج ليست حالة الجلسة: افحص قبل أي شارة.", "",
         "## بطاقات القدرات", "", "| المجموعة | العائلة | البطاقات | الأسطر | الملف |", "|---|---|---:|---:|---|"]
    for group, fam, n, ln, path in sorted(index_rows):
        I.append(f"| {groups[group]['ar']} | `{fam}` | {n:,} | {ln:,} | [{path}]({path}) |")
    I += ["", "## بطاقات الأدوات", "", "| المجال | الأدوات | الأسطر | الملف |", "|---|---:|---:|---|"]
    I += [f"| `{a}` | {n} | {ln:,} | [{p}]({p}) |" for a, n, ln, p in tool_rows]
    I += ["", "## المناهج", "", "- [أنماط الاستدلال](methods/reasoning-modes.md)", "- [النماذج الذهنية](methods/mental-models.md)",
          "- [معايير الجودة وسلالم التعافي](methods/quality-and-recovery.md)", "",
          "## الروابط الخام", "", f"- هذا الفهرس: <{RAW}README.md>", f"- أي ملف: `{RAW}<المسار>` (مثلًا `{RAW}cards/motion/transitions-cuts.md`)",
          "- النسخة المجمعة في ملف واحد: `smart_capabilities.py cards --single <الملف>`.", ""]
    pages["README.md"] = I
    return {p: "\n".join(v) + "\n" for p, v in pages.items()}


def single(pages: dict) -> str:
    order = ["README.md"] + sorted(p for p in pages if p.startswith("methods/")) + sorted(p for p in pages if p.startswith("tools/")) \
        + sorted(p for p in pages if p.startswith("cards/"))
    return "\n\n---\n\n".join(f"<!-- usip-library/{p} -->\n\n" + pages[p] for p in order)
