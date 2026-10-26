#!/usr/bin/env python3
"""يولّد هيكل نموذج مالي محرّك-الأساس في إكسل من مواصفة JSON: أوراق Assumptions وDrivers وPnL وBS وCF وChecks وSensitivity وDocs بصيغ حية ومفتاح سيناريو واصطلاحات ألوان IB.

usage: python model_builder.py spec.json --out model.xlsx
spec.json (مثال SaaS مبسّط؛ كل القيم أمثلة):
{
 "name": "Acme SaaS", "currency": "SAR", "periods": ["2026", "2027", "2028", "2029", "2030"],
 "scenarios": ["Base", "Upside", "Downside"], "active_scenario": "Base", "probabilities": [0.6, 0.25, 0.15],
 "drivers": [
   {"key": "new_customers", "label": "عملاء جدد", "values": {"Base": [120,150,180,200,220], "Upside": [150,200,250,300,340], "Downside": [90,100,110,120,130]}, "source": "خطة المبيعات 2026-03", "unit": "عميل"},
   {"key": "arpa", "label": "متوسط الإيراد لكل عميل", "values": {"Base": [1200,1260,1320,1380,1450], "Upside": [1250,1350,1450,1550,1650], "Downside": [1150,1150,1180,1200,1220]}, "unit": "SAR/سنة"},
   {"key": "churn", "label": "معدل التسرّب", "values": {"Base": [0.08,0.075,0.07,0.07,0.065], "Upside": [0.06,0.055,0.05,0.05,0.045], "Downside": [0.12,0.11,0.1,0.1,0.1]}, "unit": "%"},
   {"key": "cogs_pct", "label": "تكلفة الإيراد %", "values": {"Base": [0.25]*5, "Upside": [0.22]*5, "Downside": [0.3]*5}, "unit": "%"},
   {"key": "heads", "label": "عدد الموظفين", "values": {"Base": [12,16,20,24,28], "Upside": [14,20,26,32,38], "Downside": [10,12,14,16,18]}, "unit": "رأس"},
   {"key": "loaded_cost", "label": "التكلفة المحمّلة للموظف", "values": {"Base": [180000]*5, "Upside": [185000]*5, "Downside": [175000]*5}, "unit": "SAR/سنة"},
   {"key": "dso", "label": "DSO", "values": {"Base": [45]*5, "Upside": [40]*5, "Downside": [60]*5}, "unit": "يوم"},
   {"key": "dpo", "label": "DPO", "values": {"Base": [30]*5, "Upside": [30]*5, "Downside": [30]*5}, "unit": "يوم"},
   {"key": "capex_per_head", "label": "Capex لكل موظف", "values": {"Base": [6000]*5, "Upside": [6000]*5, "Downside": [6000]*5}, "unit": "SAR"},
   {"key": "tax_rate", "label": "الضريبة", "values": {"Base": [0.2]*5, "Upside": [0.2]*5, "Downside": [0.2]*5}, "unit": "%"}
 ],
 "opening": {"cash": 500000, "customers": 100, "equity": 500000}
}
يحتاج openpyxl. المخرج فيه صفوف BS_check وCF_check؛ افتح الملف في إكسل (أو شغّل xlsx_recalc.py) ليُعاد الحساب.
"""
import argparse
import json
import sys

try:
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
    from openpyxl.utils import get_column_letter as L
    from openpyxl.workbook.defined_name import DefinedName
except ImportError:
    sys.exit("openpyxl غير مثبت: pip install openpyxl")

BLUE = Font(color="0000FF"); BLACK = Font(color="000000"); GREEN = Font(color="008000"); BOLD = Font(bold=True)
HEAD = PatternFill("solid", fgColor="1F3864"); HEADF = Font(bold=True, color="FFFFFF"); YELLOW = PatternFill("solid", fgColor="FFF2CC")
NUM = '#,##0;[Red](#,##0);"-"'; PCT = '0.0%'; MULT = '0.0"x"'
TOP = Border(top=Side(style="thin"))


def header(ws, title, periods, first_col=3):
    ws["A1"] = title; ws["A1"].font = Font(bold=True, size=14)
    ws.sheet_view.rightToLeft = True
    for j, p in enumerate(periods):
        c = ws.cell(row=3, column=first_col + j, value=p); c.fill = HEAD; c.font = HEADF; c.alignment = Alignment(horizontal="center")
    ws.cell(row=3, column=1, value="البند").fill = HEAD; ws.cell(row=3, column=1).font = HEADF
    ws.cell(row=3, column=2, value="الوحدة/الملاحظة").fill = HEAD; ws.cell(row=3, column=2).font = HEADF
    ws.column_dimensions["A"].width = 34; ws.column_dimensions["B"].width = 22
    for j in range(len(periods)):
        ws.column_dimensions[L(first_col + j)].width = 14
    ws.freeze_panes = "C4"


def main() -> None:
    ap = argparse.ArgumentParser(); ap.add_argument("spec"); ap.add_argument("--out", default="model.xlsx")
    a = ap.parse_args()
    spec = json.load(open(a.spec, encoding="utf-8"))
    P = spec["periods"]; n = len(P); S = spec["scenarios"]; drivers = spec["drivers"]; op = spec.get("opening", {})
    wb = Workbook()

    # ── Assumptions: scenario switch + driver tables per scenario (blue inputs) ───────────────────
    ws = wb.active; ws.title = "Assumptions"; header(ws, f"{spec['name']} — الافتراضات (أزرق = مدخل؛ غيّر هنا فقط)", P)
    ws["A5"] = "السيناريو النشط"; ws["B5"] = spec.get("active_scenario", S[0]); ws["B5"].font = BLUE; ws["B5"].fill = YELLOW
    ws["A6"] = "رقم السيناريو"; ws["B6"] = f'=MATCH(B5,{{"{"\",\"".join(S)}"}},0)'; ws["B6"].font = BLACK
    wb.defined_names.add(DefinedName("Scenario", attr_text="Assumptions!$B$6"))
    ws["A7"] = "الاحتمالات";
    for k, (s, pr) in enumerate(zip(S, spec.get("probabilities", [1 / len(S)] * len(S)))):
        ws.cell(row=7, column=3 + k, value=s).font = BOLD; ws.cell(row=8, column=3 + k, value=pr).font = BLUE; ws.cell(row=8, column=3 + k).number_format = PCT
    row = 10
    driver_rows = {}  # key -> {scenario: row}
    for d in drivers:
        ws.cell(row=row, column=1, value=d["label"]).font = BOLD; ws.cell(row=row, column=2, value=d.get("unit", "")); row += 1
        for s in S:
            ws.cell(row=row, column=1, value=f"  {s}"); ws.cell(row=row, column=2, value=d.get("source", "") if s == S[0] else "")
            for j in range(n):
                c = ws.cell(row=row, column=3 + j, value=d["values"][s][j]); c.font = BLUE
                c.number_format = PCT if d.get("unit") == "%" else NUM
            driver_rows.setdefault(d["key"], {})[s] = row; row += 1
        row += 1
    # opening balances + financing (blue inputs, referenced by the statements)
    ws.cell(row=row, column=1, value="الأرصدة الافتتاحية والتمويل").font = BOLD; row += 1
    OPEN = {}
    for key, label in (("cash", "النقد الافتتاحي"), ("customers", "العملاء الافتتاحيون"), ("equity", "رأس المال")):
        ws.cell(row=row, column=1, value=label); c = ws.cell(row=row, column=3, value=op.get(key, 0)); c.font = BLUE; c.number_format = NUM
        OPEN[key] = f"Assumptions!$C${row}"; row += 1
    ws.cell(row=row, column=1, value="التدفق من التمويل (لكل فترة)"); fin_row = row
    for j in range(n):
        c = ws.cell(row=row, column=3 + j, value=0); c.font = BLUE; c.number_format = NUM
    row += 1

    # ── Drivers: live values chosen by Scenario (CHOOSE) ─────────────────────────────────────────
    wd = wb.create_sheet("Drivers"); header(wd, "المحرّكات الحيّة (تُختار بمفتاح السيناريو؛ لا تُعدَّل هنا)", P)
    live = {}
    r = 5
    for d in drivers:
        wd.cell(row=r, column=1, value=d["label"]); wd.cell(row=r, column=2, value=d.get("unit", ""))
        for j in range(n):
            refs = ",".join(f"Assumptions!{L(3 + j)}{driver_rows[d['key']][s]}" for s in S)
            c = wd.cell(row=r, column=3 + j, value=f"=CHOOSE(Scenario,{refs})"); c.font = BLACK
            c.number_format = PCT if d.get("unit") == "%" else NUM
        live[d["key"]] = r; r += 1
    def D(key, j):
        return f"Drivers!{L(3 + j)}{live[key]}"

    # ── PnL ───────────────────────────────────────────────────────────────────────────────────────
    wp = wb.create_sheet("PnL"); header(wp, "قائمة الدخل", P)
    rows = {}
    def put(ws_, r_, label, fn, fmt=NUM, bold=False, unit=""):
        ws_.cell(row=r_, column=1, value=label).font = BOLD if bold else Font(); ws_.cell(row=r_, column=2, value=unit)
        for j in range(n):
            c = ws_.cell(row=r_, column=3 + j, value=fn(j)); c.number_format = fmt; c.font = BOLD if bold else BLACK
            if bold: c.border = TOP
        return r_
    rows["cust_begin"] = put(wp, 5, "العملاء — بداية", lambda j: f"={OPEN['customers']}" if j == 0 else f"={L(2 + j)}{8}", NUM, unit="عميل")
    rows["cust_new"] = put(wp, 6, "+ جدد", lambda j: f"={D('new_customers', j)}")
    rows["cust_churn"] = put(wp, 7, "− متسرّبون", lambda j: f"=-ROUND({L(3 + j)}5*{D('churn', j)},0)")
    rows["cust_end"] = put(wp, 8, "العملاء — نهاية", lambda j: f"=SUM({L(3 + j)}5:{L(3 + j)}7)", NUM, True)
    rows["rev"] = put(wp, 10, "الإيراد", lambda j: f"=AVERAGE({L(3 + j)}5,{L(3 + j)}8)*{D('arpa', j)}", NUM, True, spec.get("currency", ""))
    rows["cogs"] = put(wp, 11, "− تكلفة الإيراد", lambda j: f"=-{L(3 + j)}10*{D('cogs_pct', j)}")
    rows["gp"] = put(wp, 12, "مجمل الربح", lambda j: f"={L(3 + j)}10+{L(3 + j)}11", NUM, True)
    rows["gm"] = put(wp, 13, "هامش مجمل الربح", lambda j: f"=IF({L(3 + j)}10=0,0,{L(3 + j)}12/{L(3 + j)}10)", PCT)
    rows["opex"] = put(wp, 15, "− المصروفات التشغيلية (رؤوس × تكلفة محمّلة)", lambda j: f"=-{D('heads', j)}*{D('loaded_cost', j)}")
    rows["dep"] = put(wp, 16, "− الإهلاك", lambda j: f"=-CF!{L(3 + j)}12*-1*0+BS!{L(3 + j)}18*-1")  # placeholder replaced below
    rows["ebit"] = put(wp, 17, "الربح التشغيلي EBIT", lambda j: f"={L(3 + j)}12+{L(3 + j)}15+{L(3 + j)}16", NUM, True)
    rows["tax"] = put(wp, 18, "− الضريبة", lambda j: f"=-MAX(0,{L(3 + j)}17)*{D('tax_rate', j)}")
    rows["ni"] = put(wp, 19, "صافي الدخل", lambda j: f"={L(3 + j)}17+{L(3 + j)}18", NUM, True)

    # ── CF ────────────────────────────────────────────────────────────────────────────────────────
    wc = wb.create_sheet("CF"); header(wc, "قائمة التدفقات النقدية", P)
    put(wc, 5, "صافي الدخل", lambda j: f"=PnL!{L(3 + j)}19")
    put(wc, 6, "+ الإهلاك", lambda j: f"=-PnL!{L(3 + j)}16")
    put(wc, 7, "− الزيادة في الذمم المدينة", lambda j: f"=-(BS!{L(3 + j)}6-{'BS!' + L(2 + j) + '6' if j else 0})")
    put(wc, 8, "+ الزيادة في الذمم الدائنة", lambda j: f"=BS!{L(3 + j)}14-{'BS!' + L(2 + j) + '14' if j else 0}")
    put(wc, 9, "التدفق من العمليات CFO", lambda j: f"=SUM({L(3 + j)}5:{L(3 + j)}8)", NUM, True)
    put(wc, 11, "− Capex", lambda j: f"=-{D('heads', j)}*{D('capex_per_head', j)}")
    put(wc, 12, "التدفق من الاستثمار CFI", lambda j: f"={L(3 + j)}11", NUM, True)
    put(wc, 14, "التدفق من التمويل CFF", lambda j: f"=Assumptions!{L(3 + j)}{fin_row}", NUM, True)
    put(wc, 16, "النقد — بداية", lambda j: f"={OPEN['cash']}" if j == 0 else f"={L(2 + j)}17")
    put(wc, 17, "النقد — نهاية", lambda j: f"={L(3 + j)}16+{L(3 + j)}9+{L(3 + j)}12+{L(3 + j)}14", NUM, True)

    # ── BS ────────────────────────────────────────────────────────────────────────────────────────
    wbs = wb.create_sheet("BS"); header(wbs, "الميزانية العمومية", P)
    put(wbs, 5, "النقد", lambda j: f"=CF!{L(3 + j)}17")
    put(wbs, 6, "الذمم المدينة (الإيراد × DSO/365)", lambda j: f"=PnL!{L(3 + j)}10*{D('dso', j)}/365")
    put(wbs, 7, "PP&E الإجمالي", lambda j: f"={'0' if j == 0 else L(2 + j) + '7'}-CF!{L(3 + j)}11")
    put(wbs, 8, "− مجمع الإهلاك", lambda j: f"={'0' if j == 0 else L(2 + j) + '8'}+PnL!{L(3 + j)}16")
    put(wbs, 9, "PP&E الصافي", lambda j: f"={L(3 + j)}7+{L(3 + j)}8")
    put(wbs, 10, "إجمالي الأصول", lambda j: f"={L(3 + j)}5+{L(3 + j)}6+{L(3 + j)}9", NUM, True)
    put(wbs, 14, "الذمم الدائنة (COGS × DPO/365)", lambda j: f"=-PnL!{L(3 + j)}11*{D('dpo', j)}/365")
    put(wbs, 15, "إجمالي الخصوم", lambda j: f"={L(3 + j)}14", NUM, True)
    put(wbs, 16, "رأس المال", lambda j: f"={OPEN['equity']}+SUM(CF!$C$14:{L(3 + j)}14)")
    put(wbs, 17, "الأرباح المحتجزة", lambda j: f"={'0' if j == 0 else L(2 + j) + '17'}+PnL!{L(3 + j)}19")
    put(wbs, 18, "الإهلاك السنوي (PP&E الإجمالي/3)", lambda j: f"={L(3 + j)}7/3")
    put(wbs, 19, "إجمالي حقوق الملكية", lambda j: f"={L(3 + j)}16+{L(3 + j)}17", NUM, True)
    put(wbs, 20, "إجمالي الخصوم وحقوق الملكية", lambda j: f"={L(3 + j)}15+{L(3 + j)}19", NUM, True)
    # fix depreciation formula now that BS!18 exists
    for j in range(n):
        wp.cell(row=16, column=3 + j, value=f"=-BS!{L(3 + j)}18")

    # ── Checks ───────────────────────────────────────────────────────────────────────────────────
    wk = wb.create_sheet("Checks"); header(wk, "الفحوص (يجب أن تكون صفراً في كل فترة)", P)
    put(wk, 5, "BS_check = الأصول − (الخصوم + حقوق الملكية)", lambda j: f"=ROUND(BS!{L(3 + j)}10-BS!{L(3 + j)}20,2)", NUM, True)
    put(wk, 6, "CF_check = نقد الميزانية − نقد التدفقات", lambda j: f"=ROUND(BS!{L(3 + j)}5-CF!{L(3 + j)}17,2)", NUM, True)
    put(wk, 7, "Customers ≥ 0", lambda j: f"=IF(PnL!{L(3 + j)}8<0,1,0)", NUM)
    wk["A9"] = "الحالة الكلية"; wk["B9"] = f'=IF(SUMPRODUCT(ABS(C5:{L(2 + n)}7))=0,"OK","ERROR")'; wk["B9"].font = BOLD; wk["B9"].fill = YELLOW

    # ── Sensitivity (2-way skeleton with instructions; Excel Data Table must be created in Excel) ──
    wsn = wb.create_sheet("Sensitivity"); wsn.sheet_view.rightToLeft = True
    wsn["A1"] = "الحساسية الثنائية: الإيراد الأخير مقابل (ARPA × التسرّب)"; wsn["A1"].font = Font(bold=True, size=14)
    wsn["A3"] = "القيمة الناتجة (ضع =PnL!آخر إيراد هنا ثم Data → What-If → Data Table بصف ARPA وعمود churn)"
    wsn["B4"] = f"=PnL!{L(2 + n)}10"; wsn["B4"].font = BLACK
    for k, v in enumerate([0.9, 0.95, 1.0, 1.05, 1.1]):
        wsn.cell(row=4, column=3 + k, value=v).font = BLUE; wsn.cell(row=4, column=3 + k).number_format = '0%" ARPA"'
    for k, v in enumerate([0.05, 0.07, 0.09, 0.11, 0.13]):
        wsn.cell(row=5 + k, column=2, value=v).font = BLUE; wsn.cell(row=5 + k, column=2).number_format = '0.0%" churn"'

    # ── Docs ─────────────────────────────────────────────────────────────────────────────────────
    wdoc = wb.create_sheet("Docs"); wdoc.sheet_view.rightToLeft = True; wdoc.column_dimensions["A"].width = 110
    for i, line in enumerate([
        f"{spec['name']} — نموذج محرّك-الأساس. العملة: {spec.get('currency', '')}. الفترات: {', '.join(P)}.",
        "الألوان: أزرق = مدخلات (Assumptions فقط)، أسود = صيغ، أصفر = افتراض حرج/مفتاح.",
        "مفتاح السيناريو: Assumptions!B5 (Base/Upside/Downside). المحرّكات الحيّة في Drivers عبر CHOOSE(Scenario,…).",
        "التكامل: صافي الدخل → الأرباح المحتجزة؛ Capex → PP&E والإهلاك → مجمع الإهلاك؛ AR = الإيراد×DSO/365؛ AP = COGS×DPO/365.",
        "الفحوص: Checks!B9 يجب أن تكون OK؛ BS_check وCF_check صفر في كل فترة. لا Plug.",
        "التحديث: سجّل التاريخ والمالك وما تغيّر هنا في كل مراجعة.",
        "القيود المعروفة: الإهلاك خطي 3 سنوات على PP&E الإجمالي؛ لا ديون ولا إيراد مؤجّل (أضفهما كصفوف بمحرّكات جديدة عند الحاجة).",
    ], 1):
        wdoc.cell(row=i, column=1, value=line)
    wb.save(a.out)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(json.dumps({"out": a.out, "sheets": wb.sheetnames, "drivers": len(drivers), "periods": n, "scenarios": S,
                      "next": "افتح في إكسل أو شغّل ../../excel-automation-power/scripts/xlsx_recalc.py ثم model_audit.py"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
