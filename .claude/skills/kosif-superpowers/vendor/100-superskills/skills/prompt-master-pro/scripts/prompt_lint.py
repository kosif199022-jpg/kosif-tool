#!/usr/bin/env python3
"""فاحص برومبتات حتمي: الأقسام الثمانية، ومخاطر الصياغة، وتسوير المدخلات، والأسرار؛ درجة من 100 وحكم PASS/REVISE/BLOCK.

usage:
  python prompt_lint.py prompt.md [--kind task|system|agent|tool] [--untrusted] [--json]
  echo "..." | python prompt_lint.py - --kind system
الخروج: 0 PASS · 1 REVISE · 3 BLOCK (سر في البرومبت، أو مدخل غير موثوق بلا تسوير، أو طلب كشف التفكير الداخلي).
يفهم العربية والإنجليزية. الدرجة تقيس الاكتمال البنيوي؛ ليست حكماً على الذكاء.
"""
import argparse
import json
import re
import sys

SECTIONS = {
    "role": (8, r"\byou are\b|\bact as\b|<role>|أنت (خبير|مساعد|محلل|مراجع|كاتب|مهندس|مدرب)|دورك|بصفتك"),
    "context": (10, r"<context>|\bcontext\b|\bbackground\b|\baudience\b|\bthe user is\b|السياق|الجمهور|الخلفية|المستخدم هو"),
    "task": (20, r"<task>|\byour task\b|\btask:|\b(write|create|analy[sz]e|classify|summari[sz]e|extract|translate|generate|review|answer|convert|plan|design|build)\b|اكتب|حلل|لخص|صنف|استخرج|ترجم|راجع|أجب|صمم|ابنِ|المهمة"),
    "inputs": (8, r"<inputs?>|<document>|<text>|<data>|\binput\b|المدخل|النص التالي|الوثيقة"),
    "constraints": (12, r"<constraints>|\bmust\b|\bshould\b|\bat most\b|\bno more than\b|\bexactly\b|\bwithin \d|\blimit\b|≤|يجب|لا تتجاوز|بحد أقصى|فقط|بالضبط"),
    "output_format": (18, r"<output_format>|\bformat\b|\bjson\b|\bschema\b|\bmarkdown\b|\btable\b|\bbullet|\bheadings?\b|\brespond with\b|\breturn only\b|التنسيق|جدول|نقاط|بصيغة|أعِد فقط|عناوين"),
    "edge_cases": (12, r"<edge_cases>|\bif (the )?(input|data|document|information|answer|text) (is )?(missing|empty|unclear|ambiguous|not)|\bif you (are unsure|don't know|cannot)|\bnot in the (document|text|context)\b|إذا (لم|كانت|كان) .{0,25}(غير|ناقص|فارغ|غامض|متاح)|إن لم تجد|غير موجود في|لا أعرف"),
    "quality_bar": (12, r"<quality_bar>|\bsuccess criteria\b|\bwill be (judged|evaluated|graded)\b|\bcheck your (answer|work)\b|\bbefore (answering|responding)\b|\bself[- ]check\b|معيار|تحقق من إجابتك|قبل الإجابة|سيُقيَّم"),
}
AGENT = {
    "stop_condition": r"\bstop (when|if)\b|\bdone when\b|\buntil\b|\bfinish(ed)? when\b|توقف (عند|إذا)|انتهِ عندما|اكتمل عندما",
    "budget": r"\bmax(imum)? (of )?\d+ (steps|calls|retries|attempts|iterations|tool calls)\b|\bbudget\b|\bat most \d+ (steps|calls|tries)|بحد أقصى \d+ (خطوات|محاولات|استدعاءات)|ميزانية",
    "checkpoints": r"\b(captcha|otp|password|credential|payment|confirm with the user|ask the user before|human approval|ask before)\b|اسأل المستخدم قبل|موافقة|تأكيد قبل|كلمة مرور|دفع",
    "postcondition": r"\bverify\b|\bconfirm (that|the result)\b|\bpostcondition\b|\bcheck that\b|\bproof\b|تحقق أن|تأكد أن|الدليل",
}
TOOL = {
    "when_to_use": r"\buse (this|it) (when|to|for)\b|\bwhen to use\b|استخدمها عند|متى تُستخدم",
    "when_not": r"\bdo not use\b|\bdon't use\b|\bwhen not to use\b|\bnot for\b|لا تستخدمها|ليست لـ",
    "parameters": r"\bparam(eter)?s?\b|\barguments?\b|\(\s*(string|int|integer|number|boolean|array|object)\s*\)|المعاملات|البارامترات",
    "side_effects": r"\bside[- ]effects?\b|\bmodifies\b|\bwrites\b|\bread[- ]only\b|\bdeletes\b|\bsends\b|\bidempotent\b|آثار جانبية|يكتب|يحذف|يرسل|للقراءة فقط",
}
VAGUE = r"\b(good|nice|better|some|various|etc\.?|stuff|things|appropriate|properly|as needed|short|long|detailed|a few|several|high[- ]quality|comprehensive)\b|\b(جيد|مناسب|بعض|إلخ|قصير|طويل|مفصل|عدة|شامل|احترافي)\b"
SECRET = r"\bsk-(?:proj-|ant-)?[A-Za-z0-9_-]{20,}|\bgh[pousr]_[A-Za-z0-9]{36,}|\bAKIA[0-9A-Z]{16}\b|-----BEGIN [A-Z ]*PRIVATE KEY-----|\bxox[baprs]-[A-Za-z0-9-]{10,}|\bAIza[0-9A-Za-z_-]{35}\b"
REVEAL = r"(show|reveal|print|output|include) (your|all|the) (full |hidden |internal )?(chain[- ]of[- ]thought|reasoning|thoughts|scratchpad)|اعرض (تفكيرك|سلسلة أفكارك) كاملة"
DELIM = r"<\w[\w-]*>[\s\S]*?</\w[\w-]*>|```[\s\S]*?```|\"\"\"[\s\S]*?\"\"\"|^###\s|^---\s*$"
PLACEHOLDER = r"\{\{?\s*[\w ]+\s*\}?\}|\[(user input|document|text|input|paste .*?|النص|الوثيقة|المدخل)\]|\$\{\w+\}|<<[^>]+>>"
NEG_ONLY = r"(?m)^\s*[-*•]?\s*(don'?t|do not|never|avoid|لا تفعل|لا تستخدم|لا تكتب|تجنب|يُمنع)\b"
POS_WITH_NEG = r"(instead|rather|بدل|بدلاً|عوضاً)"
ARABIC = r"[؀-ۿ]"
LANG_SPEC = r"\b(in (modern standard )?arabic|in english|language:|respond in|reply in)\b|باللغة العربية|بالفصحى|بالعامية|بالإنجليزية|اللغة:"


def lint(prompt: str, kind: str = "task", untrusted: bool = False) -> dict:
    p = prompt.strip()
    if not p:
        raise ValueError("prompt is empty")
    found, weights = {}, {}
    for k, (w, rx) in SECTIONS.items():
        found[k] = bool(re.search(rx, p, re.I | re.M))
        weights[k] = w
    extra = AGENT if kind == "agent" else TOOL if kind == "tool" else {}
    for k, rx in extra.items():
        found[k] = bool(re.search(rx, p, re.I | re.M))
        weights[k] = 10
    if kind == "tool":
        for k in ("role", "quality_bar", "edge_cases", "context"):
            weights.pop(k, None)
    score = round(100 * sum(w for k, w in weights.items() if found.get(k)) / sum(weights.values()))
    missing = [k for k in weights if not found.get(k)]

    issues, verdict = [], "PASS"
    order = ["PASS", "REVISE", "BLOCK"]

    def raise_to(v):
        nonlocal verdict
        verdict = max(verdict, v, key=order.index)

    if re.search(SECRET, p):
        issues.append({"severity": "BLOCK", "code": "secret", "msg": "سر أو مفتاح داخل البرومبت؛ احذفه واستخدم متغير بيئة"})
        raise_to("BLOCK")
    if re.search(REVEAL, p, re.I):
        issues.append({"severity": "BLOCK", "code": "reveal_reasoning", "msg": "يطلب كشف التفكير الداخلي؛ اطلب الاستنتاج والدليل والسبب المختصر"})
        raise_to("BLOCK")
    has_placeholder = bool(re.search(PLACEHOLDER, p))
    has_delim = bool(re.search(DELIM, p, re.M))
    if (untrusted or has_placeholder) and not has_delim:
        issues.append({"severity": "BLOCK", "code": "undelimited_input", "msg": "مدخل غير موثوق بلا تسوير؛ ضعه داخل <document>…</document> وقل إنه بيانات لا تعليمات"})
        raise_to("BLOCK")
    vague = sorted(set(m.group(0).lower() for m in re.finditer(VAGUE, p, re.I)))
    if len(vague) >= 3:
        issues.append({"severity": "REVISE", "code": "vague", "msg": f"كلمات غامضة ({', '.join(vague[:6])}): بدّلها بأسماء وأرقام (3 نقاط ≤ 15 كلمة)"})
        raise_to("REVISE")
    negs = re.findall(NEG_ONLY, p, re.I)
    if len(negs) >= 3 and not re.search(POS_WITH_NEG, p, re.I):
        issues.append({"severity": "REVISE", "code": "negative_only", "msg": f"{len(negs)} قاعدة سلبية بلا بديل إيجابي؛ كل «لا تفعل» تحتاج «افعل بدلها»"})
        raise_to("REVISE")
    caps = re.findall(r"\b[A-Z]{5,}\b", p)
    if len(caps) >= 4:
        issues.append({"severity": "REVISE", "code": "shouting", "msg": "صراخ بالأحرف الكبيرة؛ الأهمية تأتي من الترتيب والوضوح لا من الحجم"})
        raise_to("REVISE")
    if re.search(r"\balways\b", p, re.I) and re.search(r"\bnever\b", p, re.I):
        pairs = set(re.findall(r"\balways ([a-z]+)", p, re.I)) & set(re.findall(r"\bnever ([a-z]+)", p, re.I))
        if pairs:
            issues.append({"severity": "REVISE", "code": "contradiction", "msg": f"تناقض always/never على: {', '.join(pairs)}"})
            raise_to("REVISE")
    if re.search(ARABIC, p) and not re.search(LANG_SPEC, p, re.I):
        issues.append({"severity": "REVISE", "code": "language_unspecified", "msg": "اللغة غير محددة؛ قل «أجب بالعربية الفصحى» أو حدّد اللهجة"})
        raise_to("REVISE")
    words = len(p.split())
    if words > 2500:
        issues.append({"severity": "REVISE", "code": "overlong", "msg": f"{words} كلمة؛ انقل المرجعيات الطويلة إلى ملفات تُسترجع عند الحاجة"})
        raise_to("REVISE")
    if words < 25:
        issues.append({"severity": "REVISE", "code": "too_short", "msg": "أقل من 25 كلمة؛ أضف السياق والصيغة والقيود"})
        raise_to("REVISE")
    if not found.get("output_format"):
        issues.append({"severity": "REVISE", "code": "no_format", "msg": "لا صيغة إخراج؛ حدّد المخطط أو العناوين أو الطول مع مثال مملوء"})
        raise_to("REVISE")
    if not found.get("edge_cases") and kind != "tool":
        issues.append({"severity": "REVISE", "code": "no_edge_cases", "msg": "لا سلوك للحالات الحرجة؛ ماذا يفعل عند نقص البيانات أو خروج الطلب عن النطاق؟"})
        raise_to("REVISE")
    if score < 60:
        raise_to("REVISE")
    return {"verdict": verdict, "score": score, "kind": kind, "words": words, "sections_found": [k for k in weights if found.get(k)],
            "sections_missing": missing, "issues": issues,
            "next": "أصلح BLOCK أولاً، ثم أضف الأقسام الناقصة بترتيب الوزن (task، output_format، constraints، edge_cases)، ثم اختبر على 3 حالات."}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("file", help="ملف البرومبت أو - للقراءة من stdin")
    ap.add_argument("--kind", default="task", choices=("task", "system", "agent", "tool"))
    ap.add_argument("--untrusted", action="store_true", help="البرومبت سيحمل نصاً من مستخدم/ويب/ملف")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    text = sys.stdin.read() if a.file == "-" else open(a.file, encoding="utf-8").read()
    r = lint(text, a.kind, a.untrusted)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=1))
    else:
        print(f"{r['verdict']}  score={r['score']}/100  kind={r['kind']}  words={r['words']}")
        if r["sections_missing"]:
            print("ناقص:", ", ".join(r["sections_missing"]))
        for i in r["issues"]:
            print(f"- [{i['severity']}] {i['code']}: {i['msg']}")
        print(r["next"])
    sys.exit({"PASS": 0, "REVISE": 1, "BLOCK": 3}[r["verdict"]])


if __name__ == "__main__":
    main()
