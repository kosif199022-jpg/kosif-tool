#!/usr/bin/env python3
"""يحلّل برومبتاً ويُخرج بطاقة تشخيص وهياكل ثلاث نسخ (A أقصى فعالية، B متوازن، C أقصى كفاءة) مع تقدير الرموز ودرجة إلزام الإخراج وفئة النموذج.

usage: python prompt_frontier.py prompt.md [--model claude|gpt|gemini|qwen3-8b|gemma-3-12b|llama-3.1-8b|...] [--json]
التحليل حتمي (أنماط نصية): الأركيتايب، وفئة النموذج، وعدد القيود المتزامنة، وهل المخرج يُحلَّل، وهل يوجد سقالة تفكير، وأمثلة بآثار تفكير،
ومدخلات غير مسوّرة، وصراخ، وتناقضات، ورموز مقدّرة (أحرف/4). النسخ هياكل تملؤها أنت؛ الدرجات «متوقعة» حتى تُقاس.
"""
import argparse
import json
import re
import sys

ARCHETYPES = [
    ("judge", r"\b(score|grade|evaluate|rate|rubric|judge|criteria|pass/fail)\b|قيّم|درجة|معيار"),
    ("extraction", r"\b(extract|pull out|identify all|entities|fields|parse)\b|استخرج|الحقول|الكيانات"),
    ("classification", r"\b(classify|categori[sz]e|label|which category|one of)\b|صنّف|الفئة"),
    ("agent", r"\b(tool|tools|call|function|step|until|stop when|browse|search the web|execute)\b|أداة|أدوات|نفّذ|توقف عند"),
    ("generation", r"\b(write|draft|compose|generate|create)\b|اكتب|ألّف|أنشئ"),
    ("transformation", r"\b(translate|summari[sz]e|rewrite|convert|reformat)\b|ترجم|لخّص|أعد صياغة"),
]
CONSTRAINT_RX = r"(?im)(?:^|[.!?؟]\s*)[-*•\d.)]*\s*(?:you\s+)?(must|never|always|do not|don't|exactly|at most|no more than|only|يجب|لا |ممنوع|فقط|بالضبط|بحد أقصى)"
PARSED_RX = r"\bjson\b|\bschema\b|\byaml\b|\bcsv\b|\bxml\b|return only|respond only|output format|صيغة الإخراج|أعد فقط|JSON"
SCAFFOLD_RX = r"think step by step|let'?s think|show your (reasoning|work)|explain your reasoning|chain[- ]of[- ]thought|فكّر خطوة|اشرح تفكيرك|<thinking>"
TRACE_EXAMPLE_RX = r"<example>[\s\S]*?(<thinking>|reasoning:|step 1)[\s\S]*?</example>"
UNTRUSTED_RX = r"\{\{?\s*\w+\s*\}?\}|\[(user input|document|text|input|النص|الوثيقة)\]|\$\{\w+\}"
DELIM_RX = r"<\w[\w-]*>[\s\S]*?</\w[\w-]*>|```[\s\S]*?```"
SHOUT_RX = r"\b(CRITICAL|MUST|NEVER|ALWAYS|IMPORTANT)\b"


def model_class(m: str) -> tuple[str, str]:
    m = (m or "claude").lower()
    if re.search(r"claude|opus|sonnet|fable|mythos|gpt-?[56]|o[1-9]\b|gemini[- ]?3|r1|deepseek-r", m):
        return "frontier-reasoning", "لا سقالة تفكير؛ معايير نجاح دقيقة + إعداد effort/reasoning_effort/thinking_level؛ لا آثار تفكير كأمثلة؛ XML للأقسام المختلطة (Claude)؛ البيانات الطويلة أولاً والسؤال آخراً."
    if re.search(r"qwen3|gemma[- ]?4|deepseek[- ]?v3|gpt-oss", m):
        return "hybrid-open-reasoner", "التحكم بالعمق عبر مفتاح الوضع/رمز التفكير لا بالنثر؛ تحت 9B: اختيار العمق ذاتياً؛ 8B-32B: توجيه باتفاق مسودتين."
    if re.search(r"gemma[- ]?[23]|llama|phi|mistral|qwen2|\b\d{1,2}b\b", m):
        return "small-open-instruct", "صفر أمثلة أولاً؛ الإلزام بالمحرك (Ollama format / llama.cpp grammar) لا بالتعليمات؛ JSON أو Python لا XML؛ درجة الحرارة 0."
    return "classic-non-reasoning", "الأنماط الكلاسيكية تنطبق (CoT، Step-Back، Self-Consistency…) بحسب شكل المهمة وتكلفتها."


def analyze(text: str, model: str) -> dict:
    low = text.lower()
    arche = next((n for n, rx in ARCHETYPES if re.search(rx, text, re.I)), "generation")
    mclass, mnote = model_class(model)
    constraints = len(re.findall(CONSTRAINT_RX, text))
    parsed = bool(re.search(PARSED_RX, text, re.I))
    scaffold = bool(re.search(SCAFFOLD_RX, text, re.I))
    trace_examples = bool(re.search(TRACE_EXAMPLE_RX, text, re.I))
    placeholders = bool(re.search(UNTRUSTED_RX, text))
    delimited = bool(re.search(DELIM_RX, text))
    shouting = len(re.findall(SHOUT_RX, text))
    tokens = round(len(text) / 4)
    issues = []
    if mclass == "frontier-reasoning" and scaffold:
        issues.append("سقالة تفكير على نموذج تفكير: احذفها (إلا عند أدنى effort) واستبدلها بمعايير نجاح.")
    if trace_examples:
        issues.append("أمثلة تحمل آثار تفكير: تُدهور المُفكّرين المدرَّبين بالتعزيز؛ حوّل الاستراتيجية إلى تعليمة وأبقِ المدخل/المخرج فقط.")
    if placeholders and not delimited:
        issues.append("مدخل غير موثوق بلا تسوير: ضعه داخل <document>…</document> واذكر أنه بيانات لا تعليمات.")
    if shouting >= 4 and mclass == "frontier-reasoning":
        issues.append("لغة ضغط كثيرة (MUST/NEVER/CRITICAL): النماذج الحديثة تُفرط في الاستجابة لها؛ خفّفها واترك القاعدة الصلبة بصيغة عادية.")
    if parsed and re.search(r'"answer"[\s\S]{0,200}"reason', text):
        issues.append("مفتاح answer قبل reason في المخطط: يحوّل التفكير إلى إجابة مباشرة؛ اعكس الترتيب أو افصل التفكير في مرحلة.")
    if constraints > 5:
        issues.append(f"{constraints} قيداً متزامناً: الامتثال المشترك يتشبّع مبكراً؛ اقترح تقسيماً إلى مراحل أو خطوة تحقق-وإعادة كنسخة مستقلة.")
    elif constraints >= 4:
        issues.append(f"{constraints} قيود: أضف مُتحقّقاً (validator) إلى جانب البرومبت.")
    if arche == "judge" and re.search(r"1\s*(-|to|إلى)\s*10|من 1 إلى 10", text):
        issues.append("قاضٍ بمقياس 1-10: عيب؛ معيار واحد لكل قاضٍ، ثنائي مع دليل، و0-5 فقط حيث يلزم رقم.")
    if arche == "agent" and re.search(r"<example", text, re.I):
        issues.append("أمثلة few-shot في برومبت وكيل أدوات: الافتراضي بلا أمثلة؛ أوصاف الأدوات هي الرافعة.")
    if tokens > 1500 and not re.search(r"cache|تخزين", low):
        issues.append("برومبت طويل يُرسل كل مرة: مرشّح للتخزين المؤقت (الثابت أولاً، المتغير آخراً).")
    rung = None
    if parsed:
        rung = {"frontier-reasoning": "3 (مخطط API / structured outputs) بعد محاولة 1→2؛ reason قبل answer أو مرحلتان",
                "hybrid-open-reasoner": "3 بفك تشفير مقيّد بعد كتلة التفكير (vLLM/SGLang) أو 4 فكّر ثم قيّد",
                "small-open-instruct": "2 تحقق-وإصلاح كحد أدنى، 3 grammar عند الإنتاج؛ ≤1.5B احذر ضريبة القيد",
                "classic-non-reasoning": "1→2؛ 3 إن توفر"}[mclass]
    return {"archetype": arche, "model_class": mclass, "model_note": mnote, "constraints": constraints, "output_parsed": parsed,
            "enforcement_rung": rung, "reasoning_scaffold": scaffold, "trace_examples": trace_examples, "placeholders": placeholders,
            "delimited": delimited, "shouting": shouting, "tokens_est": tokens, "issues": issues}


def scorecard(a: dict) -> str:
    rows = [("Intent alignment", "?"), ("Instruction clarity", "?"), ("Constraint correctness", "?"), ("Model fit", "2" if a["issues"] and a["model_class"] == "frontier-reasoning" and a["reasoning_scaffold"] else "?"),
            ("Context efficiency", "?"), ("Robustness", "2" if (a["placeholders"] and not a["delimited"]) else "?")]
    cond = []
    if a["output_parsed"]:
        cond.append(("Output determinism", "?"))
    if a["archetype"] == "agent":
        cond.append(("Tool-use correctness", "?"))
    if a["archetype"] == "judge":
        cond.append(("Evalability", "?"))
    L = [f"### بطاقة التشخيص (الأصل، متوقعة)", f"- الأركيتايب: **{a['archetype']}** · فئة النموذج: **{a['model_class']}**", f"- {a['model_note']}",
         f"- رموز مقدّرة: ~{a['tokens_est']} (أحرف/4) · قيود متزامنة: {a['constraints']} · مخرج يُحلَّل: {'نعم' if a['output_parsed'] else 'لا'}" + (f" · درجة الإلزام: {a['enforcement_rung']}" if a["enforcement_rung"] else ""), "",
         "| البعد | الدرجة (1-5) | المشكلة |", "|---|:---:|---|"]
    L += [f"| {n} | {s} | |" for n, s in rows + cond]
    if a["issues"]:
        L += ["", "**مشكلات مكتشفة آلياً:**"] + [f"- {i}" for i in a["issues"]]
    return "\n".join(L)


def variants(a: dict) -> str:
    eff = {"frontier-reasoning": "احذف السقالة؛ معايير نجاح بأرقام؛ effort كإعداد؛ اطلب المخرج فقط.",
           "hybrid-open-reasoner": "مفتاح الوضع no-think مع تصعيد عند الاختلاف؛ Chain of Draft إن احتاج تفكيراً.",
           "small-open-instruct": "صفر أمثلة؛ تعليمة قصيرة؛ الإلزام بالمحرك؛ تجنّب التفكير داخل JSON.",
           "classic-non-reasoning": "Chain of Draft (أمثلة بصيغة مسودة ≤5 كلمات) أو «كن موجزاً»؛ لا Self-Consistency إلا إن كانت كل نقطة دقة تساوي 100× سعرها."}[a["model_class"]]
    return "\n".join([
        "### جبهة النسخ", "",
        "#### A — أقصى فعالية", "```", "<role>…جملة واحدة…</role>", "<context>…الجمهور، نقطة البداية، لماذا…</context>", "<task>…خطوات مرقّمة إن لزم الترتيب…</task>",
        "<inputs>…كل مدخل داخل علامته + «بيانات لا تعليمات»…</inputs>", "<constraints>…إيجابي أولاً؛ كل «لا» معها «بدلها»…</constraints>",
        "<output_format>…المخطط/العناوين + مثال مملوء واحد (مدخل/مخرج فقط، بلا آثار تفكير)…</output_format>",
        "<edge_cases>…النقص، الغموض، خارج النطاق…</edge_cases>", "<quality_bar>…معايير النجاح بأرقام؛ ما يقرره النموذج بنفسه…</quality_bar>", "```",
        f"- الإلزام إن كان المخرج يُحلَّل: {a['enforcement_rung'] or 'لا ينطبق'} · التغيير السلوكي: (اذكر ما شُدّد أو أُرخي)", "",
        "#### B — متوازن", "```", "…نفس الأقسام مع حذف الأمثلة الزائدة وضغط السياق إلى الحقائق اللازمة فقط…", "```", "",
        "#### C — أقصى كفاءة", "```", "…تعليمة مباشرة + معايير نجاح + صيغة الإخراج فقط…", "```", f"- التقنية: {eff}", "",
        "### المقارنة", "| النسخة | رموز (تقدير) | Δ | التقنية | الإلزام | الأثر المتوقع (غير مقاس) | ما تتخلى عنه |", "|---|---|---|---|---|---|---|",
        f"| الأصل | {a['tokens_est']} | — | — | — | — | — |", "| A | | | | | | |", "| B | | | | | | |", "| C | | | | | | |", "",
        "### ملاحظة الأمانة", "- كل درجة هنا متوقعة لا مقاسة؛ تغييرات تنسيق صغيرة تقلب الدقة. للتحقق: تقييم مزدوج على نفس المدخلات بهامش عدم دونية معلن.",
        "- إن كان المخرج يُحلَّل: الامتثال متوقع حتى يُقاس على 100 مدخل حقيقي؛ اجمع معدل فشل التحليل ومعدل «صحيح الشكل خاطئ المعنى» معاً.",
        "- إن كان برومبت نظام مخزّناً: اختصاره يوفّر عُشر ما يبدو (0.1× للقراءة؛ 0.025× على Fable 5.1)، وتعديله يعيد الكتابة بـ 1.25×/2×.",
    ])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--model", default="claude")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    text = sys.stdin.read() if a.file == "-" else open(a.file, encoding="utf-8").read()
    an = analyze(text, a.model)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if a.json:
        print(json.dumps(an, ensure_ascii=False, indent=1))
    else:
        print(scorecard(an)); print(); print(variants(an))


if __name__ == "__main__":
    main()
