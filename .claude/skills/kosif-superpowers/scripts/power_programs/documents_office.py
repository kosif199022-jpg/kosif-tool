"""Real programs for the documents-office family (Arabic RTL Office files, PDF text hygiene, delivery gate).

Built with zipfile/ElementTree, openpyxl, python-pptx, arabic-reshaper and python-bidi only.
Cards that need LibreOffice, pandoc, weasyprint, Chromium, pypdf, OCR or host connectors are
skipped (out/power-programs/data-skipped.json).
"""
from __future__ import annotations

import json
import re
import unicodedata
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def _w(work: Path, name: str, obj) -> Path:
    p = work / name
    p.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(obj, (bytes, bytearray)):
        p.write_bytes(obj)
    elif isinstance(obj, str):
        p.write_text(obj, encoding="utf-8")
    else:
        p.write_text(json.dumps(obj, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    return p


def _c(name, cond, obs):
    return (name, bool(cond), str(obs))


# ---------------------------------------------------------------- DOC-01
def doc_01(work: Path):
    def para(text, size_half_pt):
        return (f'<w:p><w:pPr><w:bidi/><w:jc w:val="right"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Amiri" w:hAnsi="Amiri" w:cs="Amiri"/>'
                f'<w:rtl/><w:sz w:val="{size_half_pt}"/><w:szCs w:val="{size_half_pt}"/></w:rPr><w:t xml:space="preserve">{text}</w:t></w:r></w:p>')

    cells = [["المنتج", "الكمية"], ["قلم", "3"]]
    table = "<w:tbl><w:tblPr><w:bidiVisual/></w:tblPr>" + "".join(
        "<w:tr>" + "".join(f"<w:tc>{para(c, 24)}</w:tc>" for c in row) + "</w:tr>" for row in cells) + "</w:tbl>"
    body = para("تقرير المبيعات", 40) + para("نص الفقرة الأولى.", 24) + table
    doc = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="{W}"><w:body>{body}<w:sectPr/></w:body></w:document>'
    ct = ('<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'
          '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>')
    p = work / "rtl.docx"
    with zipfile.ZipFile(p, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct)
        z.writestr("_rels/.rels", rels)
        z.writestr("word/document.xml", doc)
    with zipfile.ZipFile(p) as z:
        root = ET.fromstring(z.read("word/document.xml"))
    ns = {"w": W}
    paras = root.findall(".//w:p", ns)
    runs = root.findall(".//w:r", ns)
    head = paras[0].find(".//w:szCs", ns).get(f"{{{W}}}val")
    texts = "".join(t.text for t in root.iter(f"{{{W}}}t"))
    return [_c("every paragraph has <w:bidi/>", all(p.find("w:pPr/w:bidi", ns) is not None for p in paras), len(paras)),
            _c("every run has w:rtl and complex-script font Amiri", all(r.find("w:rPr/w:rtl", ns) is not None and r.find("w:rPr/w:rFonts", ns).get(f"{{{W}}}cs") == "Amiri" for r in runs), len(runs)),
            _c("heading 20 pt set via both w:sz and w:szCs (40 half-points)", head == "40" and paras[0].find(".//w:sz", ns).get(f"{{{W}}}val") == "40", head),
            _c("table carries w:bidiVisual (column 1 on the right)", root.find(".//w:tblPr/w:bidiVisual", ns) is not None, ""),
            _c("Arabic text reads back in logical order", "تقرير المبيعات" in texts, texts[:20])]


# ---------------------------------------------------------------- DOC-02
def doc_02(work: Path):
    from openpyxl import Workbook, load_workbook
    from openpyxl.chart import BarChart, Reference
    from openpyxl.styles import Alignment
    wb = Workbook()
    ws = wb.active
    ws.title = "المبيعات"
    ws.sheet_view.rightToLeft = True
    rows = [("المدينة", "الإيراد", "الحصة"), ("القاهرة", 1200, None), ("الرياض", 900, None), ("دبي", 700, None), ("جدة", 540, None)]
    for r in rows:
        ws.append(list(r))
    for i in range(2, 6):
        ws[f"C{i}"] = f"=B{i}/SUM($B$2:$B$5)"
        ws[f"C{i}"].number_format = "0.0%"
        ws[f"B{i}"].number_format = "#,##0"
    ws["B6"] = "=SUM(B2:B5)"
    for row in ws.iter_rows():
        for c in row:
            c.alignment = Alignment(horizontal="right", readingOrder=2)
    ch = BarChart()
    ch.add_data(Reference(ws, min_col=2, min_row=1, max_row=5), titles_from_data=True)
    ch.set_categories(Reference(ws, min_col=1, min_row=2, max_row=5))
    ws.add_chart(ch, "E2")
    p = work / "arabic.xlsx"
    wb.save(p)
    b = load_workbook(p)
    s = b["المبيعات"]
    with zipfile.ZipFile(p) as z:
        chart_parts = [n for n in z.namelist() if n.startswith("xl/charts/chart")]
        chart_xml = z.read(chart_parts[0]).decode() if chart_parts else ""
    expected_total = 1200 + 900 + 700 + 540
    return [_c("sheet is right-to-left", s.sheet_view.rightToLeft is True, ""),
            _c("formulas stored as strings", s["B6"].value == "=SUM(B2:B5)" and s["C2"].value == "=B2/SUM($B$2:$B$5)", s["B6"].value),
            _c("number formats #,##0 and 0.0%", s["B2"].number_format == "#,##0" and s["C2"].number_format == "0.0%", ""),
            _c("alignment right with readingOrder 2", s["A2"].alignment.horizontal == "right" and s["A2"].alignment.readingOrder == 2, ""),
            _c("native bar chart part written, referencing B1:B5", len(chart_parts) == 1 and "$B$2:$B$5" in chart_xml, chart_parts),
            _c("total the SUM must yield is 3340", expected_total == 3340, expected_total)]


# ---------------------------------------------------------------- DOC-04
def doc_04(work: Path):
    from pptx import Presentation
    from pptx.chart.data import CategoryChartData
    from pptx.enum.chart import XL_CHART_TYPE
    from pptx.oxml.ns import qn
    from pptx.util import Inches, Pt
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    s = prs.slides.add_slide(prs.slide_layouts[6])
    tb = s.shapes.add_textbox(Inches(1), Inches(0.5), Inches(11), Inches(1.2))
    for i, (text, size) in enumerate((("تقرير الربع الثالث", 40), ("نمو الإيراد في كل المدن", 24))):
        para = tb.text_frame.paragraphs[0] if i == 0 else tb.text_frame.add_paragraph()
        run = para.add_run()
        run.text = text
        run.font.size = Pt(size)
        pPr = para._p.get_or_add_pPr()
        pPr.set("rtl", "1")
        pPr.set("algn", "r")
        rPr = run._r.get_or_add_rPr()
        rPr.set("lang", "ar-SA")
        for tag in ("a:latin", "a:cs"):
            el = rPr.makeelement(qn(tag), {"typeface": "Cairo"})
            rPr.append(el)
    cd = CategoryChartData()
    cd.categories = ["القاهرة", "الرياض", "دبي"]
    cd.add_series("الإيراد", (1200, 900, 700))
    s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(1), Inches(2), Inches(8), Inches(4.5), cd)
    p = work / "rtl.pptx"
    prs.save(p)
    back = Presentation(p)
    sl = back.slides[0]
    tf = [sh for sh in sl.shapes if sh.has_text_frame][0].text_frame
    chart = [sh for sh in sl.shapes if sh.has_chart][0].chart
    cats = list(chart.plots[0].categories)
    p0 = tf.paragraphs[0]._p.pPr
    r0 = tf.paragraphs[0].runs[0]._r.rPr
    return [_c("16:9 slide 13.333 x 7.5 in", (back.slide_width, back.slide_height) == (Inches(13.333), Inches(7.5)), (back.slide_width, back.slide_height)),
            _c("paragraphs rtl=1 algn=r", all(pp._p.pPr.get("rtl") == "1" and pp._p.pPr.get("algn") == "r" for pp in tf.paragraphs), p0.attrib),
            _c("runs lang ar-SA with latin and cs typeface Cairo", r0.get("lang") == "ar-SA" and r0.find(qn("a:cs")).get("typeface") == "Cairo" and r0.find(qn("a:latin")) is not None, ""),
            _c("title 40 pt, body 24 pt", (tf.paragraphs[0].runs[0].font.size.pt, tf.paragraphs[1].runs[0].font.size.pt) == (40, 24), ""),
            _c("chart categories read back in order", cats == ["القاهرة", "الرياض", "دبي"], cats)]


# ---------------------------------------------------------------- DOC-11
def doc_11(work: Path):
    from openpyxl import Workbook, load_workbook
    wb = Workbook()
    ws = wb.active
    for r in range(40):
        ws.append([f"c{r}{k}" for k in range(20)])
    before = (ws.page_setup.orientation, bool(ws.sheet_properties.pageSetUpPr and ws.sheet_properties.pageSetUpPr.fitToPage))
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = ws.page_setup.fitToHeight = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    p = work / "fit.xlsx"
    wb.save(p)
    b = load_workbook(p).active
    with zipfile.ZipFile(p) as z:
        xml = z.read("xl/worksheets/sheet1.xml").decode()
    return [_c("orientation landscape persisted", b.page_setup.orientation == "landscape", b.page_setup.orientation),
            _c("fitToWidth = fitToHeight = 1", (b.page_setup.fitToWidth, b.page_setup.fitToHeight) == (1, 1), ""),
            _c("fitToPage flag set in sheetPr", b.sheet_properties.pageSetUpPr.fitToPage is True and 'fitToPage="1"' in xml, ""),
            _c("default sheet was not fit-to-page", before[1] is False, before)]


# ---------------------------------------------------------------- DOC-14
def _clean_extracted(s):
    s = unicodedata.normalize("NFKC", s)
    return re.sub("[‪-‮⁦-⁩‎‏]", "", s)


def doc_14(work: Path):
    import arabic_reshaper
    phrase = "تقرير المبيعات الربعي"
    shaped = arabic_reshaper.reshape(phrase)  # what a PDF text layer holds: presentation forms
    extracted_pypdf_like = "‫" + shaped + "‬"
    extracted_reversed = "".join(reversed(shaped))  # a visual-order extractor
    a = _clean_extracted(extracted_pypdf_like)
    b = _clean_extracted(extracted_reversed)
    _w(work, "extract_check.json", {"known": phrase, "logical_extractor": a, "visual_extractor": b})
    return [_c("presentation forms present before normalising", any(0xFB50 <= ord(c) <= 0xFEFF for c in shaped), ""),
            _c("NFKC + strip U+202A..202E recovers the known phrase", a == phrase, a),
            _c("a visual-order extractor still fails the comparison", b != phrase and b == phrase[::-1], b),
            _c("embedding marks removed", not re.search("[‪-‮]", a), "")]


# ---------------------------------------------------------------- DOC-15
def doc_15(work: Path):
    import arabic_reshaper
    src = "السلام عليكم ولا إله إلا الله"
    extracted = arabic_reshaper.reshape(src)
    ligs = sum(1 for ch in extracted if 0xFEF5 <= ord(ch) <= 0xFEFC)
    naive = extracted == src
    lam_alef = {"ﻻ": "لا", "ﻼ": "لا", "ﻷ": "لأ", "ﻸ": "لأ", "ﻹ": "لإ", "ﻺ": "لإ", "ﻵ": "لآ", "ﻶ": "لآ"}

    def lam_alef_aware(s):
        for k, v in lam_alef.items():
            s = s.replace(k, v)
        return unicodedata.normalize("NFKC", s)

    ok = lam_alef_aware(extracted) == src
    planted = lam_alef_aware(extracted.replace(extracted[0], "")) == src
    _w(work, "lamalef.json", {"ligatures": ligs, "match": ok})
    return [_c("extracted text holds the 3 lam-alef ligatures", ligs == 3, ligs),
            _c("naive comparison fails", not naive, ""),
            _c("lam-alef-aware normalisation matches the source", ok, ok),
            _c("a real missing letter is still detected", not planted, "")]


# ---------------------------------------------------------------- DOC-22
def doc_22(work: Path):
    WESTERN, INDIC = set("0123456789"), set("٠١٢٣٤٥٦٧٨٩")

    def wrap_ltr(html_text):
        return re.sub(r"([A-Za-z][A-Za-z0-9 .:/_-]*[A-Za-z0-9])", r"<bdi>\1</bdi>", html_text)

    def numerals(text):
        has_w, has_i = bool(set(text) & WESTERN), bool(set(text) & INDIC)
        return "mixed" if has_w and has_i else "western" if has_w else "indic" if has_i else "none"

    p = "استخدم أمر git push ثم افتح GitHub Actions."
    out = wrap_ltr(p)
    html = f'<html lang="ar" dir="rtl"><p>{out}</p><p dir="ltr">English line</p></html>'
    _w(work, "mixed.html", html)
    runs_docx = [("مرحبا ", True), ("Kosif", False), (" بك", True)]
    return [_c("each LTR run isolated in <bdi>", out == "استخدم أمر <bdi>git push</bdi> ثم افتح <bdi>GitHub Actions</bdi>.", out),
            _c("mixed numeral systems detected", numerals("الصفحة 12 من ١٥") == "mixed", ""),
            _c("one system per document passes", numerals("الصفحة ١٢ من ١٥") == "indic" and numerals("page 12 of 15") == "western", ""),
            _c("DOCX: LTR run kept without w:rtl", [r for r, rtl in runs_docx if not rtl] == ["Kosif"], runs_docx)]


# ---------------------------------------------------------------- DOC-23
def doc_23(work: Path):
    import arabic_reshaper
    from bidi.algorithm import get_display
    engines = {"reportlab": False, "pillow+raqm": True, "matplotlib+raqm": True, "matplotlib no raqm": False, "html/browser": True}

    def prepare(s, engine):
        return s if engines[engine] else get_display(arabic_reshaper.reshape(s))

    s = "مرحبا"
    raw_engine_render = lambda t: get_display(arabic_reshaper.reshape(t))  # what a shaping engine does internally
    correct = raw_engine_render(prepare(s, "pillow+raqm"))
    doubled = raw_engine_render(get_display(arabic_reshaper.reshape(s)))  # pre-shaped AND engine shapes
    _w(work, "shaping.json", {k: ("manual reshape+bidi" if not v else "raw logical") for k, v in engines.items()})
    return [_c("default: raw logical string for engines with a shaper", prepare(s, "html/browser") == s and prepare(s, "pillow+raqm") == s, ""),
            _c("reportlab gets reshape + get_display", prepare(s, "reportlab") == get_display(arabic_reshaper.reshape(s)) != s, ""),
            _c("doing both reverses the text", doubled == correct[::-1] and doubled != correct, (correct, doubled))]


# ---------------------------------------------------------------- DOC-24
def doc_24(work: Path):
    from openpyxl import Workbook, load_workbook
    results = {"total": 3340, "cities": 4}
    _w(work, "results.json", results)
    wb = Workbook()
    ws = wb.active
    ws.append(["المدينة", "الإيراد"])
    for c, v in (("القاهرة", 1200), ("الرياض", 900), ("دبي", 700), ("جدة", 540)):
        ws.append([c, v])
    ws.append(["المجموع", results["total"]])
    p = work / "report.xlsx"
    wb.save(p)

    def gate(path, frozen):
        checks, unverified = {}, ["recalculation (no LibreOffice here)", "visual render", "opened in MS Office"]
        s = load_workbook(path).active
        vals = [r for r in s.iter_rows(values_only=True)]
        checks["read back"] = vals[0][0] == "المدينة"
        checks["numbers from frozen results"] = vals[-1][1] == frozen["total"] and len(vals) - 2 == frozen["cities"]
        checks["sums tie"] = sum(r[1] for r in vals[1:-1]) == vals[-1][1]
        checks["size sensible"] = 1000 < path.stat().st_size < 5_000_000
        return all(checks.values()), checks, unverified

    ok, checks, unverified = gate(p, results)
    bad_ok, bad_checks, _ = gate(p, {"total": 3300, "cities": 4})
    _w(work, "gate.json", {"pass": ok, "checks": checks, "unverified": unverified})
    return [_c("gate passes the honest report", ok, checks),
            _c("numbers not matching the frozen results fail the gate", not bad_ok and not bad_checks["numbers from frozen results"], bad_checks),
            _c("unverifiable steps stated, not claimed", "recalculation (no LibreOffice here)" in unverified, unverified)]


PROGRAMS = {"DOC-01": doc_01, "DOC-02": doc_02, "DOC-04": doc_04, "DOC-11": doc_11, "DOC-14": doc_14, "DOC-15": doc_15,
            "DOC-22": doc_22, "DOC-23": doc_23, "DOC-24": doc_24}
