"""model_audit.py must count a constant planted where a formula belongs and fail the verdict."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

try:
    import openpyxl
except ImportError:  # pragma: no cover
    openpyxl = None

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".claude/skills/kosif-superpowers/vendor/100-superskills/skills/excel-model-architect/scripts"
AUDIT = SCRIPTS / "model_audit.py"
BUILDER = SCRIPTS / "model_builder.py"
SPEC = SCRIPTS.parent / "templates" / "spec.example.json"


def _audit(path):
    p = subprocess.run([sys.executable, str(AUDIT), str(path), "--json"], capture_output=True, text=True, encoding="utf-8")
    return p.returncode, json.loads(p.stdout)


@unittest.skipIf(openpyxl is None, "openpyxl not installed")
class ExcelModelAuditTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def _small_model(self, planted=False):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Assumptions"
        ws["A3"], ws["C3"], ws["D3"], ws["E3"], ws["F3"] = "Item", "2026", "2027", "2028", "2029"
        ws["A5"] = "Price"
        for col, v in zip("CDEF", (10, 11, 12, 13)):
            ws[f"{col}5"] = v  # input block on the inputs sheet: legitimate
        pnl = wb.create_sheet("PnL")
        pnl["A5"], pnl["A6"] = "Units", "Revenue"
        pnl["C5"] = 100  # opening value followed by formulas: legitimate
        for prev, col in zip("CDE", "DEF"):
            pnl[f"{col}5"] = f"={prev}5+Assumptions!{col}5"
        for col in "CDEF":
            pnl[f"{col}6"] = f"={col}5*Assumptions!{col}5"
        if planted:
            pnl["E6"] = 4321
        chk = wb.create_sheet("Checks")
        chk["A5"], chk["C5"] = "BS_check", "=0"
        wb.defined_names["Scenario"] = openpyxl.workbook.defined_name.DefinedName("Scenario", attr_text="Assumptions!$C$5")
        path = self.tmp / ("planted.xlsx" if planted else "clean.xlsx")
        wb.save(path)
        return path

    def test_small_clean_model_passes(self):
        code, rep = _audit(self._small_model())
        self.assertEqual(rep["verdict"], "PASS", rep["findings"])
        self.assertEqual(rep["stats"]["hardcoded"], 0)
        self.assertEqual(code, 0)

    def test_small_planted_constant_fails(self):
        code, rep = _audit(self._small_model(planted=True))
        self.assertGreaterEqual(rep["stats"]["hardcoded"], 1)
        self.assertNotEqual(rep["verdict"], "PASS")
        self.assertNotEqual(code, 0)
        self.assertTrue(any(f["cell"] == "PnL!E6" and f["sev"] == "HIGH" for f in rep["findings"]), rep["findings"])
        self.assertFalse(any(f["cell"] == "PnL!C5" and f["sev"] == "HIGH" for f in rep["findings"]),
                         "opening value must not be counted as a hardcode")
        self.assertEqual(rep["stats"]["hardcoded"], 1)

    def test_built_model_clean_then_planted(self):
        model = self.tmp / "model.xlsx"
        subprocess.run([sys.executable, str(BUILDER), str(SPEC), "--out", str(model)], check=True, capture_output=True)
        code, rep = _audit(model)
        self.assertEqual(rep["verdict"], "PASS", rep["findings"])
        self.assertEqual(rep["stats"]["hardcoded"], 0)
        self.assertEqual(code, 0)
        wb = openpyxl.load_workbook(model)
        cell = next(c for row in wb["PnL"].iter_rows(min_col=4) for c in row
                    if isinstance(c.value, str) and c.value.startswith("="))
        cell.value = 12345
        planted = self.tmp / "planted.xlsx"
        wb.save(planted)
        code, rep = _audit(planted)
        self.assertGreaterEqual(rep["stats"]["hardcoded"], 1)
        self.assertNotEqual(rep["verdict"], "PASS")
        self.assertEqual(code, 1)
        self.assertTrue(any(f["cell"] == f"PnL!{cell.coordinate}" for f in rep["findings"]))


if __name__ == "__main__":
    unittest.main()
