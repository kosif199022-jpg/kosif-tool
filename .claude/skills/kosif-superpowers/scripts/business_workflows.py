#!/usr/bin/env python3
"""KOSIF business workflows: Futurepedia 'For Business' + 64 workflow playbooks, run Claude-natively.

Registry: data/futurepedia_business_workflows.json (facts only; no third-party prompts stored).
Every step names a third-party tool on the source site; this tool re-routes each step to what
Claude/KOSIF can do itself (write, research, data, slides, design, docs, transcribe, video, build,
automate) or to a connector, and marks the steps that need the user's approval (send, post, spend,
record people).

Commands
  functions                  9 business functions with adoption %, tool categories, matching workflows
  roles                      workflow counts per role
  list [--role R]            the 64 workflows (36 library FW-xx + 28 creator playbooks FP-xx)
  search "<words>"           Arabic/English search
  show <id|slug>             one workflow with its routed steps
  coverage                   how much of each workflow Claude can do natively vs. via connectors
  plan --workflow ID --context "<user situation>" --out FILE.md
                             a Claude-native runbook (steps, executor, approval gates, deliverables)
"""
import argparse
import json
import re
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
DATA = SKILL / "data" / "futurepedia_business_workflows.json"
NATIVE = {"write", "research", "data", "slides", "design", "docs", "transcribe", "video", "build"}
APPROVAL = {"crm_comms": "يرسل/ينشر/يحدّث نظامًا خارجيًا — يحتاج موافقة صريحة لكل إرسال",
            "voice_avatar": "صوت أو وجه أو إنفاق — موافقة صريحة وموافقة صاحب الصوت/الصورة",
            "automate": "أتمتة دائمة أو مجدولة — موافقة قبل التفعيل",
            "transcribe": "تسجيل أشخاص — موافقة كل المشاركين",
            "manual": "خطوة يدوية يقوم بها المستخدم"}
ALIASES = {"مبيعات": "sales", "تسويق": "marketer", "محتوى": "content", "فيديو": "video", "بودكاست": "podcast",
           "اجتماع": "meeting", "توظيف": "hiring recruiter", "مستثمر": "investor", "عرض": "deck presentation",
           "بحث": "research", "بيانات": "data", "تصميم": "design", "هوية": "brand", "دعم": "support customer",
           "بريد": "email", "إيميل": "email", "موقع": "landing page website", "تطبيق": "app tool", "أتمتة": "automate",
           "مؤسس": "founder", "وكالة": "agency", "تعلم": "learn", "يوتيوب": "youtube", "منافس": "competitive"}


def load(path=DATA):
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    if d.get("schema") != "kosif.business.workflows.v1":
        raise ValueError("unexpected schema")
    w = d["workflows"]
    if len(w) != 64 or len({x["id"] for x in w}) != 64 or len({x["slug"] for x in w}) != 64:
        raise ValueError("registry must hold 64 unique workflows")
    for x in w:
        for s in x["steps"]:
            if s["route"] not in d["routes"]:
                raise ValueError("unknown route " + s["route"])
    if len(d["business_functions"]) != 9:
        raise ValueError("expected 9 business functions")
    return d


def resolve(d, token):
    t = token.strip().casefold()
    m = [x for x in d["workflows"] if t in (x["id"].casefold(), x["slug"], x["name"].casefold())]
    if len(m) != 1:
        raise ValueError("unknown or ambiguous workflow: " + token)
    return m[0]


def search(d, q):
    q = q.strip().casefold()
    if not 1 <= len(q) <= 200:
        raise ValueError("query must be 1-200 characters")
    for ar, en in ALIASES.items():
        if ar in q:
            q += " " + en
    words = [w for w in re.split(r"[^\w؀-ۿ]+", q) if len(w) >= 2]
    out = []
    for x in d["workflows"]:
        hay = " ".join([x["id"], x["slug"], x["name"], x["role"], x["role_ar"], x["goal"], x.get("creator") or ""] +
                       [s["title"] + " " + s["source_tool"] for s in x["steps"]]).casefold()
        score = sum(3 if w in x["name"].casefold() else 1 for w in words if w in hay)
        if score:
            out.append((score, x["id"], x))
    return [x for _, _, x in sorted(out, key=lambda r: (-r[0], r[1]))]


def coverage(x):
    n = len(x["steps"])
    native = sum(1 for s in x["steps"] if s["route"] in NATIVE)
    gated = [s["route"] for s in x["steps"] if s["route"] in APPROVAL]
    return {"id": x["id"], "name": x["name"], "steps": n, "claude_native": native, "native_pct": round(100 * native / n),
            "needs_approval_or_connector": len(gated)}


def plan(d, x, context):
    if not isinstance(context, str) or not 1 <= len(context.strip()) <= 3000:
        raise ValueError("context must have 1-3000 characters")
    R = d["routes"]
    c = coverage(x)
    L = ["# خطة تشغيل Claude — %s (%s)" % (x["name"], x["id"]), "",
         "**الهدف:** %s · **الدور:** %s · **الوقت المرجعي:** %s · **المستوى:** %s" % (x["goal"], x["role_ar"], x["duration"], x["difficulty"]),
         "**سياقك:** " + context.strip(),
         "**التغطية:** %d من %d خطوات ينفذها Claude بنفسه (%d%%)، و%d خطوة تحتاج موافقتك أو موصّلًا." % (c["claude_native"], c["steps"], c["native_pct"], c["needs_approval_or_connector"]),
         "", "| # | الخطوة | الأداة في المصدر | من ينفذ هنا | البوابة |", "|---|---|---|---|---|"]
    for i, s in enumerate(x["steps"], 1):
        r = R[s["route"]]
        gate = APPROVAL.get(s["route"], "مراجعة المخرَج قبل الخطوة التالية")
        L.append("| %d | %s | %s | %s — %s | %s |" % (i, s["title"], s["source_tool"], r["ar"], r["executor"], gate))
    L += ["", "## قواعد التنفيذ",
          "- كل خطوة تسلّم مخرَجًا ملموسًا (ملف، مستند، جدول، مسودة) يُراجع قبل التي بعدها.",
          "- لا إرسال ولا نشر ولا تحديث لنظام خارجي ولا إنفاق ولا تسجيل أشخاص إلا بموافقة صريحة لكل فعل.",
          "- جرّب الأتمتة على بيانات تجريبية غير حساسة أولًا، وتحقق من كل ادعاء ومصدر.",
          "- اختر خطوة تالية واحدة قابلة للتراجع عند الشك.",
          "- عند غياب موصّل لخدمة مذكورة: ابحث في سجل الموصّلات، وإلا جهّز المسودة ليقوم بها المستخدم.",
          "", "_Status: PLAN_ONLY — لم يُنفَّذ شيء بعد. المصدر: %s (أسماء الخطوات والأدوات فقط؛ لا برومبتات منسوخة)._" % x["source_url"]]
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("functions"); sub.add_parser("roles"); sub.add_parser("coverage")
    ls = sub.add_parser("list"); ls.add_argument("--role")
    sr = sub.add_parser("search"); sr.add_argument("query")
    sh = sub.add_parser("show"); sh.add_argument("workflow")
    pl = sub.add_parser("plan"); pl.add_argument("--workflow", required=True); pl.add_argument("--context", required=True); pl.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    try:
        d = load()
        W = d["workflows"]
        if a.cmd == "functions":
            res = [{k: f[k] for k in ("id", "name", "name_ar", "adoption_pct", "use", "kosif_workflows")} for f in sorted(d["business_functions"], key=lambda f: -f["adoption_pct"])]
        elif a.cmd == "roles":
            res = {}
            for x in W:
                res[x["role"]] = res.get(x["role"], 0) + 1
        elif a.cmd == "list":
            res = [{"id": x["id"], "name": x["name"], "role": x["role"], "goal": x["goal"], "duration": x["duration"]} for x in W if not a.role or x["role"] == a.role]
        elif a.cmd == "search":
            res = [{"id": x["id"], "name": x["name"], "goal": x["goal"]} for x in search(d, a.query)[:10]]
        elif a.cmd == "show":
            x = resolve(d, a.workflow); res = dict(x, coverage=coverage(x))
        elif a.cmd == "coverage":
            res = sorted((coverage(x) for x in W), key=lambda c: -c["native_pct"])
        else:
            x = resolve(d, a.workflow)
            out = Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
            with out.open("x", encoding="utf-8") as f:
                f.write(plan(d, x, a.context))
            res = {"status": "PLAN_CREATED_NOT_EXECUTED", "file": str(out), "workflow": x["id"]}
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, KeyError, OSError, json.JSONDecodeError) as e:
        print("BUSINESS_WORKFLOWS_ERROR: " + str(e), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
