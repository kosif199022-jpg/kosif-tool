import sys, pathlib, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from glass_memory_probe import probe,simulate
from matrices import generate
class TestMatrices(unittest.TestCase):
    def test_glass_counterfactual_is_repeatable(self):
        self.assertEqual(probe(),probe())
        self.assertTrue(probe()["causal_difference_detected"])
        self.assertTrue(probe()["same_material_memory"])
        self.assertNotEqual(simulate(False)[0],simulate(True)[0])
    def test_requires_86_provenance(self):
        from matrices import load_catalog
        import tempfile,json
        with tempfile.TemporaryDirectory() as d:
            f=pathlib.Path(d)/"short.json";f.write_text(json.dumps({"styles":[]}))
            with self.assertRaises(ValueError):load_catalog(f)
    def test_same_seed_generates_same_records(self):
        rows=[]
        for i in range(86):
            rows.append({"style_id":str(i),"card_family":str(i//6),
                "operator_tags":[["grid","shape","mesh"][i%3],["flow","pulse","trace"][i%3],["glow","grain","gradient"][i%3]]})
        self.assertEqual(generate(rows,5,42),generate(rows,5,42))
if __name__=="__main__":unittest.main()
