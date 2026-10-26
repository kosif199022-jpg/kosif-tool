#!/usr/bin/env python3
"""بوابة إعادة الحساب: يعيد حساب مصنّف إكسل بـ LibreOffice headless (إن وُجد)، ويمسح أخطاء الخلايا (#REF! #DIV/0! #VALUE! #N/A #NAME? #NUM!)، ويصدّر PDF للفحص البصري.

usage: python xlsx_recalc.py model.xlsx [--pdf] [--timeout 60]
بلا LibreOffice: يفحص القيم المحفوظة فقط ويصرّح أن إعادة الحساب لم تتم (status: not_recalculated).
المخرج JSON: status ok | errors_found | not_recalculated، وقائمة الخلايا المخالفة.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

try:
    from openpyxl import load_workbook
except ImportError:
    sys.exit("openpyxl غير مثبت: pip install openpyxl")

ERR = {"#REF!", "#N/A", "#VALUE!", "#DIV/0!", "#NAME?", "#NUM!", "#NULL!"}
SOFFICE_CANDIDATES = ["soffice", "libreoffice", r"C:\Program Files\LibreOffice\program\soffice.exe", r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
                      "/Applications/LibreOffice.app/Contents/MacOS/soffice"]


def find_soffice():
    for c in SOFFICE_CANDIDATES:
        p = shutil.which(c) if not os.path.isabs(c) else (c if os.path.exists(c) else None)
        if p:
            return p
    return None


def scan(path):
    wb = load_workbook(path, data_only=True); bad = []; formulas_cached = 0; empty_cached = 0
    wbf = load_workbook(path, data_only=False)
    for ws in wbf.worksheets:
        wv = wb[ws.title]
        for row in ws.iter_rows():
            for c in row:
                if isinstance(c.value, str) and c.value.startswith("="):
                    v = wv[c.coordinate].value
                    if v is None:
                        empty_cached += 1
                    else:
                        formulas_cached += 1
                    if isinstance(v, str) and v in ERR:
                        bad.append({"sheet": ws.title, "cell": c.coordinate, "error": v, "formula": c.value[:90]})
    return bad, formulas_cached, empty_cached


def main() -> None:
    ap = argparse.ArgumentParser(); ap.add_argument("file"); ap.add_argument("--pdf", action="store_true"); ap.add_argument("--timeout", type=int, default=90)
    a = ap.parse_args()
    src = os.path.abspath(a.file); soffice = find_soffice(); recalculated = False; pdf = None
    if soffice:
        tmp = tempfile.mkdtemp(prefix="recalc_")
        # convert xlsx -> xlsx forces a load+recalc+save in LibreOffice
        r = subprocess.run([soffice, "--headless", "--norestore", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", tmp, src],
                           capture_output=True, text=True, timeout=a.timeout)
        out = os.path.join(tmp, os.path.basename(src))
        if r.returncode == 0 and os.path.exists(out):
            shutil.copyfile(out, src); recalculated = True
        if a.pdf:
            r2 = subprocess.run([soffice, "--headless", "--norestore", "--convert-to", "pdf", "--outdir", os.path.dirname(src), src], capture_output=True, text=True, timeout=a.timeout)
            cand = os.path.splitext(src)[0] + ".pdf"
            pdf = cand if r2.returncode == 0 and os.path.exists(cand) else None
        shutil.rmtree(tmp, ignore_errors=True)
    bad, cached, empty = scan(src)
    status = "errors_found" if bad else ("ok" if recalculated or (cached and not empty) else "not_recalculated")
    rep = {"file": src, "recalculated": recalculated, "engine": soffice or None, "status": status, "formulas_with_cached_values": cached,
           "formulas_without_values": empty, "errors": bad[:100], "pdf": pdf,
           "note": None if recalculated else "LibreOffice غير موجود: افتح الملف في إكسل واحفظه ثم أعد الفحص؛ لا تُعلن «لا أخطاء» قبل ذلك"}
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(json.dumps(rep, ensure_ascii=False, indent=1))
    sys.exit(0 if status == "ok" else 1 if status == "errors_found" else 2)


if __name__ == "__main__":
    main()
