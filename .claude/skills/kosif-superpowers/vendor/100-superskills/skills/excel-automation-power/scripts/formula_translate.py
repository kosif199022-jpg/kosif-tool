#!/usr/bin/env python3
"""يترجم صيغ إكسل إلى Google Sheets أو Lark (فيشو) والعكس: يحوّل الدوال المختلفة، ويلفّ عمليات المصفوفات بـ ARRAYFORMULA عند الحاجة، ويحذّر مما لا يُترجم (مراجع هيكلية، @، #، LET/LAMBDA في Lark، DAY(b-a)).

usage:
  python formula_translate.py --to sheets "=SUM(Table1[Amount])*1.15"
  python formula_translate.py --to lark   --file formulas.txt [--out translated.md]
  python formula_translate.py --to excel  "=ARRAYFORMULA(A2:A100*B2:B100)"
الترجمة نحوية؛ تحقق ثلاثي قبل التسليم: دلالة Excel = حساب Python = قيمة المنصة على 3-5 صفوف ممثّلة.
"""
import argparse
import json
import re
import sys

ARRAY_NATIVE = {"ARRAYFORMULA", "FILTER", "UNIQUE", "SORT", "SORTBY", "SORTN", "SEQUENCE", "MAP", "REDUCE", "SCAN", "BYROW", "BYCOL", "MAKEARRAY",
                "XLOOKUP", "VSTACK", "HSTACK", "TOCOL", "TOROW", "TEXTSPLIT", "SPLIT", "TRANSPOSE", "SUMPRODUCT", "MMULT", "FREQUENCY", "QUERY", "CHOOSECOLS", "CHOOSEROWS", "TAKE", "DROP", "WRAPROWS", "WRAPCOLS", "EXPAND"}
SCALAR_OPS = re.compile(r"[A-Z]+\$?\d+:\$?[A-Z]+\$?\d+\s*[\+\-\*/\^=<>]|[\+\-\*/\^=<>]\s*\$?[A-Z]+\$?\d+:\$?[A-Z]+\$?\d+")
RENAME = {
    "sheets": {"TEXTJOIN": "TEXTJOIN", "CONCAT": "CONCATENATE", "IFS": "IFS", "SWITCH": "SWITCH", "XLOOKUP": "XLOOKUP", "STOCKHISTORY": None, "WEBSERVICE": None,
               "DAYS": "DAYS", "NETWORKDAYS.INTL": "NETWORKDAYS.INTL", "TEXTBEFORE": None, "TEXTAFTER": None, "TEXTSPLIT": "SPLIT", "LET": "LET", "LAMBDA": "LAMBDA"},
    "lark": {"LET": None, "LAMBDA": "LAMBDA(inline only)", "TEXTSPLIT": "SPLIT", "TEXTBEFORE": None, "TEXTAFTER": None, "STOCKHISTORY": None, "WEBSERVICE": None, "FORECAST.ETS": None,
             "CUBEVALUE": None, "INFO": None, "RTD": None, "PHONETIC": None, "AMORDEGRC": None, "GOOGLEFINANCE": None, "GOOGLETRANSLATE": None, "IMPORTRANGE": "IMPORTRANGE(≤5 nested, ≤100/sheet)"},
    "excel": {"ARRAYFORMULA": "", "SPLIT": "TEXTSPLIT", "QUERY": None, "IMPORTRANGE": None, "GOOGLEFINANCE": None, "REGEXEXTRACT": None, "REGEXMATCH": None, "REGEXREPLACE": None, "FLATTEN": "TOCOL"},
}
UNSUPPORTED_NOTE = {"QUERY": "استخدم FILTER/SORT/UNIQUE أو Power Query", "IMPORTRANGE": "Power Query من ملف آخر", "REGEXEXTRACT": "TEXTBEFORE/TEXTAFTER أو LET+MID/FIND", "REGEXMATCH": "ISNUMBER(SEARCH())", "REGEXREPLACE": "SUBSTITUTE",
                    "TEXTBEFORE": "LEFT+FIND", "TEXTAFTER": "MID+FIND", "LET": "صيغة متداخلة أو عمود مساعد", "STOCKHISTORY": "استيراد يدوي", "WEBSERVICE": "لا مكافئ", "FORECAST.ETS": "FORECAST.LINEAR أو TREND"}


def translate(formula: str, to: str):
    f = formula.strip(); warnings = []; out = f
    if not out.startswith("="):
        out = "=" + out
    # structured references Table[Col]
    if re.search(r"\w+\[[^\]]+\]", out):
        warnings.append("مرجع هيكلي Table[Col]: غير مدعوم خارج إكسل؛ استبدله بنطاق A1 صريح (مثال A2:A100)")
        out = re.sub(r"(\w+)\[\[?([^\]]+?)\]?\]", r"\2_RANGE", out)
    if to in ("sheets", "lark"):
        if "@" in out:
            warnings.append("@ التقاطع الضمني: احذفه؛ الصيغ العادية تُسقط (project) على الصف الحالي افتراضياً"); out = out.replace("@", "")
        if re.search(r"[A-Z]+\d+#", out):
            warnings.append("مرجع # للمصفوفة المنسكبة: غير مدعوم؛ استخدم نطاقاً صريحاً أو TAKE/DROP/ARRAY_CONSTRAIN"); out = re.sub(r"([A-Z]+\d+)#", r"\1:\1_SPILL", out)
        if re.search(r"\b(DAY|MONTH|YEAR)\(\s*[A-Z]+\d+\s*-\s*[A-Z]+\d+\s*\)", out):
            warnings.append("DAY(b-a) يفسّر الفرق كرقم تاريخ تسلسلي؛ استخدم DAYS(b,a) أو DATEDIF(a,b,\"M\"/\"Y\") أو b-a")
        if to == "lark" and re.search(r"[A-Z]+\d+:[A-Z]+(?![\d])|\b\d+:\d+\b", out):
            warnings.append("Lark: النطاقات المفتوحة H2:H و2:2 ممنوعة داخل الصيغة؛ استخدم H:H أو نطاقاً صريحاً")
        funcs = set(re.findall(r"\b([A-Z][A-Z0-9\.]+)\s*\(", out))
        for fn in funcs:
            rep = RENAME[to].get(fn, fn)
            if rep is None:
                warnings.append(f"{fn}: غير مدعوم في {to}؛ البديل: {UNSUPPORTED_NOTE.get(fn, 'عمود مساعد')}")
            elif rep != fn and "(" not in rep:
                out = re.sub(rf"\b{fn}\s*\(", rep + "(", out)
            elif "(" in rep and rep != fn:
                warnings.append(f"{fn}: {rep}")
        # ARRAYFORMULA wrapping when scalar ops on ranges and no native array function
        has_native = any(fn in ARRAY_NATIVE for fn in funcs)
        if SCALAR_OPS.search(out) and not has_native and not out.upper().startswith("=ARRAYFORMULA"):
            out = "=ARRAYFORMULA(" + out[1:] + ")"; warnings.append("لُفّت بـ ARRAYFORMULA: عمليات على نطاقات بلا دالة مصفوفات أصلية (وإلا تُسقط على الصف الحالي)")
        if to == "lark" and re.search(r"\b(SUMIF|COUNTIF|SUMIFS|AVERAGEIF)\s*\(\s*(INDEX|INDIRECT|OFFSET)\(", out, re.I):
            warnings.append("Lark: دالة نطاق خارجية تأكل نطاقاً من INDEX/INDIRECT/OFFSET لا تتوسع ثانية؛ استخدم MAP(ARRAYFORMULA(ROW(...)),LAMBDA(r, ...))")
        if "{=" in formula:
            warnings.append("CSE القديمة {=...}: اكتبها =ARRAYFORMULA(...)")
    else:  # to excel
        funcs = set(re.findall(r"\b([A-Z][A-Z0-9\.]+)\s*\(", out))
        for fn in funcs:
            rep = RENAME["excel"].get(fn, fn)
            if rep is None:
                warnings.append(f"{fn}: لا مكافئ مباشر في إكسل؛ البديل: {UNSUPPORTED_NOTE.get(fn, 'Power Query')}")
            elif rep == "":
                out = re.sub(r"\bARRAYFORMULA\((.*)\)\s*$", r"\1", out); warnings.append("ARRAYFORMULA حُذفت: إكسل 365 ينسكب تلقائياً (Excel 2019 وأقدم يحتاج CSE)")
            elif rep != fn:
                out = re.sub(rf"\b{fn}\s*\(", rep + "(", out)
    return out, warnings


def main() -> None:
    ap = argparse.ArgumentParser(); ap.add_argument("formula", nargs="?"); ap.add_argument("--to", required=True, choices=["sheets", "lark", "excel"])
    ap.add_argument("--file"); ap.add_argument("--out")
    a = ap.parse_args()
    items = [l.strip() for l in open(a.file, encoding="utf-8") if l.strip()] if a.file else [a.formula]
    rows = [{"source": f, "translated": t, "warnings": w} for f in items for t, w in [translate(f, a.to)]]
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if a.out:
        md = [f"# ترجمة الصيغ إلى {a.to}", "", "| الأصل | الترجمة | تحذيرات |", "|---|---|---|"]
        md += [f"| `{r['source']}` | `{r['translated']}` | {'<br>'.join(r['warnings']) or '—'} |" for r in rows]
        md += ["", "## التحقق الثلاثي (إلزامي)", "1. اختر 3-5 صفوف ممثّلة (أول/وسط/أخير/فارغ/شاذ).", "2. احسب الدلالة الأصلية بـ Python.", "3. اكتب الترجمة في المنصة واقرأ القيم.", "4. تطابق الثلاثة = تسليم؛ وإلا فالمشكلة في المصفوفات أو التواريخ أو النطاقات."]
        open(a.out, "w", encoding="utf-8").write("\n".join(md) + "\n")
    print(json.dumps(rows, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
