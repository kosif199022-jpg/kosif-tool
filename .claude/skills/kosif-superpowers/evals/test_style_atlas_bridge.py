"""Offline acceptance tests for 15 original visual-style workflow methods."""
import json
import math
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
SK=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(SK/"scripts"))
import style_atlas_bridge as A

class StyleBridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=A.registry()
        cls.styles=cls.data["styles"]

    def test_exact_source_scope(self):
        self.assertEqual(len(self.styles),15)
        self.assertEqual([x["id"] for x in self.styles],["FA-"+str(i).zfill(2) for i in range(1,16)])
        self.assertIn("FIRST_15",self.data["scope"])
        self.assertTrue(all(s["executor_verified"] is False for s in self.styles))

    def test_reference_selector_all(self):
        for style in self.styles:
            self.assertEqual(A.resolve(self.styles,style["slug"]),style)
            self.assertEqual(A.resolve(self.styles,style["id"]),style)

    def test_search_arabic_and_english(self):
        self.assertEqual(A.search(self.styles,"whiteboard")[0]["slug"],"whiteboard-explainer")
        self.assertEqual(A.search(self.styles,"سبورة")[0]["slug"],"whiteboard-explainer")
        self.assertEqual(A.search(self.styles,"مائي")[0]["slug"],"watercolor-wash")
        self.assertEqual(A.search(self.styles,"منظور")[0]["slug"],"isometric-pastel")

    def test_all_fifteen_generate_valid_distinct_svg(self):
        unique=set()
        for style in self.styles:
            svg=A.svg_study(style,"تعلم فن الرسم")
            root=ET.fromstring(svg)
            self.assertEqual(root.attrib["width"],"440")
            self.assertEqual(root.attrib["height"],"500")
            self.assertIn("original procedural schematic",svg)
            unique.add(svg)
        self.assertEqual(len(unique),15)

    def test_svg_escapes_hostile_input(self):
        svg=A.svg_study(self.styles[0],'</text><script>alert(1)</script>')
        self.assertNotIn("<script>",svg)
        self.assertIn("&lt;script&gt;",svg)
        ET.fromstring(svg)

    def test_one_style_recipe_typed_graph(self):
        obj=A.plan("شرح الاستحقاق", [self.styles[3]], duration=18,aspect="9:16")
        self.assertEqual(obj["status"],"PLAN_ONLY_NOT_RENDERED")
        self.assertEqual(len(obj["workflow"]),5)
        self.assertEqual(obj["technique_fusion"]["secondary_id"],None)
        self.assertFalse(obj["workflow"][-1]["verified"])
        self.assertIn("ANALYSIS_ONLY",obj["katana_policy"])

    def test_fusion_weights_two_distinct_styles(self):
        recipe=A.plan("Intro",[self.styles[3],self.styles[5]],duration=25,aspect="16:9")
        self.assertEqual([s["mix_weight"] for s in recipe["styles"]],[.85,.15])
        self.assertTrue(recipe["technique_fusion"]["visual_conflict_review_required"])
        self.assertEqual(recipe["styles"][1]["id"],"FA-06")

    def test_refuse_duplicates_and_invalids(self):
        with self.assertRaises(ValueError):
            A.plan("bad",[self.styles[0],self.styles[0]])
        with self.assertRaises(ValueError):
            A.plan("bad",[],duration=12)
        for x in (float("nan"),float("inf"),0,300):
            with self.assertRaises(ValueError):
                A.plan("test",[self.styles[0]],duration=x)
        with self.assertRaises(ValueError):
            A.resolve(self.styles,"FA-86")

    def test_cli_safe_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"render.svg"
            a=["study-svg","--style","FA-04","--topic","Test","--out",str(path)]
            self.assertEqual(A.main(a),0)
            self.assertEqual(A.main(a),2)
            ET.parse(path)

    def test_registry_fails_closed_on_claim_inflation(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"bad.json"
            data=json.loads(json.dumps(self.data))
            data["styles"][0]["executor_verified"]=True
            p.write_text(json.dumps(data),encoding="utf-8")
            with self.assertRaises(ValueError): A.registry(p)

if __name__=="__main__":
    unittest.main()
