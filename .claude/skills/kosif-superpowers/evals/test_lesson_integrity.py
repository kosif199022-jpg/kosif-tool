"""Tests for the lesson integrity checker; synthetic data in temp folders only, nothing is executed."""
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))
import lesson_integrity as li

REGISTRY = {
    "sources": {"spec": {"title": "Physics specification", "url": "https://example.org/spec.pdf"},
                "food": {"title": "Food table", "citation": "Food table, 2026 edition"}},
    "values": {
        "shelf": {"value": 1.5, "unit": "m", "what": "shelf height",
                  "source": {"ref": "spec", "quote": "a shelf 1.5 m above the floor"}},
        "toast": {"value": 1210, "unit": "kJ", "what": "energy in 100 g of toast",
                  "source": {"ref": "food", "quote": "Energy 1,210 kJ per 100 g"},
                  "note": "the published figure, not 290 kcal x 4.184"},
        "butter": {"value": 3000, "unit": "kJ", "what": "energy in 100 g of butter",
                   "source": {"ref": "food", "quote": "Energy 3000 kJ"}},
        "both": {"value": 4210, "unit": "kJ", "what": "toast and butter",
                 "derived": {"op": "sum", "of": ["toast", "butter"]}},
        "eff": {"value": 0.25, "unit": "fraction", "what": "bulb efficiency",
                "source": {"ref": "spec", "quote": "an efficiency of 25%"}},
        "bike": {"value": None, "unit": "kg", "what": "bicycle mass", "gap": "no cited mass for an ordinary bicycle"},
    },
}


class ValuesTests(unittest.TestCase):
    def test_clean_registry_passes_with_counts(self):
        errors, warnings, summary = li.check_values(REGISTRY)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        self.assertEqual(summary, {"sources": 2, "values": 6, "sourced": 4, "gap": 1, "derived": 1})

    def test_untraceable_number_is_an_error(self):
        reg = json.loads(json.dumps(REGISTRY))
        reg["values"]["mystery"] = {"value": 42, "unit": "J", "what": "a guess"}
        errors = li.check_values(reg)[0]
        self.assertTrue(any("no source and no gap" in e for e in errors), errors)

    def test_quote_must_support_the_number(self):
        reg = json.loads(json.dumps(REGISTRY))
        reg["values"]["butter"]["value"] = 2999
        warnings = li.check_values(reg)[1]
        self.assertTrue(any("does not appear in its quote" in w for w in warnings), warnings)

    def test_out_of_range_and_bad_derived(self):
        reg = json.loads(json.dumps(REGISTRY))
        reg["values"]["shelf"]["range"] = [2, 3]
        reg["values"]["both"]["value"] = 4200
        errors = li.check_values(reg)[0]
        self.assertTrue(any("outside its range" in e for e in errors))
        self.assertTrue(any("the sum of" in e for e in errors))

    def test_unknown_source_ref(self):
        reg = json.loads(json.dumps(REGISTRY))
        reg["values"]["shelf"]["source"]["ref"] = "blog"
        self.assertTrue(any("not in sources" in e for e in li.check_values(reg)[0]))


class RenderTests(unittest.TestCase):
    def test_placeholders_fill(self):
        text, errors = li.render(REGISTRY, "From {v:shelf} up; {n:toast} kJ; {v:eff}; {v:shelf|2}.")
        self.assertEqual(errors, [])
        self.assertEqual(text, "From 1.5 m up; 1,210 kJ; 25%; 1.50 m.")

    def test_missing_value_gap_and_unit_fail_closed(self):
        reg = json.loads(json.dumps(REGISTRY))
        reg["values"]["g"] = {"value": 9.8, "unit": "N/kg", "what": "g", "gap": "x"}
        _, errors = li.render(reg, "{v:nope} {v:bike} {v:g}")
        self.assertEqual(errors, ["no value 'nope' in the registry", "value 'bike' is a gap and cannot be shown",
                                  "no print form for unit 'N/kg' (value 'g')"])

    def test_strict_flags_typed_numbers(self):
        _, errors = li.render(REGISTRY, "The book falls {v:shelf}.\nIt hits at 5.4 m/s.", strict=True)
        self.assertEqual(len(errors), 1)
        self.assertIn("line 2", errors[0])

    def test_cli_writes_nothing_on_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            reg, content, out = Path(tmp, "v.json"), Path(tmp, "c.md"), Path(tmp, "o.md")
            reg.write_text(json.dumps(REGISTRY), encoding="utf-8")
            content.write_text("{v:nope}", encoding="utf-8")
            with redirect_stdout(io.StringIO()):
                code = li.main(["render", "--registry", str(reg), "--content", str(content), "--out", str(out)])
            self.assertEqual(code, 1)
            self.assertFalse(out.exists())


class LedgerScaleSpriteTests(unittest.TestCase):
    def test_ledger_balances_and_reports_efficiency(self):
        errors, rep = li.check_ledger({"unit": "J", "in": {"gravitational": 14.7},
                                       "out": {"kinetic": 11.0, "thermal": 3.2, "sound": 0.5},
                                       "useful": ["kinetic"], "tolerance": 1e-6})
        self.assertEqual(errors, [])
        self.assertAlmostEqual(rep["efficiency"], 11.0 / 14.7)

    def test_ledger_missing_and_negative(self):
        errors, _ = li.check_ledger({"unit": "J", "in": {"chemical": 100}, "out": {"thermal": 90, "light": -1}})
        self.assertTrue(any("negative" in e for e in errors))
        self.assertTrue(any("unaccounted for" in e for e in errors))

    def test_nice_scale(self):
        self.assertEqual([li.nice_scale(x)["capacity"] for x in (0.03, 1, 1.9, 4.6, 14.7, 4210)],
                         [0.05, 2, 5, 10, 20, 5000])
        with self.assertRaises(ValueError):
            li.nice_scale(0)

    def test_sprite_layers_overlap_and_licences(self):
        manifest = {"sounds": {"kettle": {"loop": True, "layers": {"heat": [[0.0, 2.0]], "boil": [[2.1, 1.0]]}},
                               "click": {"variants": [[3.0, 0.2]]}}}
        credits = "| Cue | Used | Source | Licence |\n|---|---|---|---|\n| `kettle` | k | s | CC0 1.0 |\n| `click` | c | s | All rights reserved |\n"
        errors, info = li.check_sprite(manifest, credits, duration=3.1)
        self.assertEqual(info["regions"], 3)
        self.assertTrue(any("not on the allowed list" in e for e in errors))
        self.assertTrue(any("past the file" in e for e in errors))

    def test_self_test(self):
        with redirect_stdout(io.StringIO()):
            self.assertEqual(li.main(["--self-test"]), 0)


if __name__ == "__main__":
    unittest.main()
