"""Atlas-5000 coverage map: fixed fixtures plus a read-only check of the shipped index. No network, no execution."""
import gzip
import json
import sys
import tempfile
import unittest
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK / "scripts"))
import atlas_5000 as a5  # noqa: E402


def skill(i, theme, verdict="READ_ONLY_OK", copyleft=False, risk=(), name="s", desc=""):
    return {"id": i, "plugin": f"p{i}", "skill": name, "theme": theme, "theme2": "", "desc": desc,
            "license": "MIT", "verdict": verdict, "copyleft": copyleft, "risk": list(risk),
            "path": f"skills/{i}-p{i}/{i}-{name}", "md_bytes": 4000, "desc_dupes": 0}


class Atlas5000Tests(unittest.TestCase):
    def setUp(self):
        self.idx = {"count": 5, "skills": [
            skill(1, "video-motion", name="webtoon-pages", desc="draw a webtoon with a fixed character"),
            skill(2, "video-motion", name="ffmpeg-cut", desc="cut video on keyframes"),
            skill(3, "security", name="secret-scan", desc="scan commits for secrets"),
            skill(4, "security", verdict="REVIEW_BEFORE_INSTALL", name="unsafe"),
            skill(5, "security", copyleft=True, name="gpl"),
        ]}
        self.cov = {"skills/1-p1/1-webtoon-pages": ["ACRAFT-09"]}

    def test_safe_core_rule(self):
        self.assertEqual([s["id"] for s in a5.safe_skills(self.idx)], [1, 2, 3])

    def test_stats_and_gaps(self):
        st = a5.stats(self.idx, self.cov)
        self.assertEqual(st["safe_core"], 3)
        self.assertEqual(st["covered"], 1)
        self.assertEqual(st["themes"]["video-motion"], {"safe": 2, "covered": 1, "coverage_pct": 50.0})
        g = a5.gaps(self.idx, self.cov, top=2)
        self.assertEqual({r["theme"] for r in g}, {"video-motion", "security"})
        for r in g:
            self.assertTrue(all(not c["covered_by"] for c in r["next_candidates"]))

    def test_find_arabic_alias_and_uncovered(self):
        hits = a5.find(self.idx, self.cov, "ارسم ويبتون", top=5)
        self.assertEqual(hits[0]["id"], 1)
        self.assertEqual(hits[0]["covered_by"], ["ACRAFT-09"])
        self.assertEqual(a5.find(self.idx, self.cov, "webtoon", uncovered_only=True), [])
        self.assertEqual(a5.find(self.idx, self.cov, ""), [])

    def test_coverage_map_reads_proof_links(self):
        with tempfile.TemporaryDirectory() as d:
            rec = {"id": "X-1", "proof": ["https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2-p2/2-ffmpeg-cut"]}
            (Path(d) / "x.json").write_text(json.dumps([rec]))
            self.assertEqual(a5.coverage_map(Path(d)), {"skills/2-p2/2-ffmpeg-cut": ["X-1"]})

    def test_shipped_index_and_new_cards(self):
        idx = a5.load_index()
        cov = a5.coverage_map()
        st = a5.stats(idx, cov)
        self.assertEqual(st["atlas_total"], 14793)
        self.assertGreater(st["safe_core"], 5000)
        receipt = json.loads((SK / "data" / "atlas-5000-mining-20261023.json").read_text(encoding="utf-8"))
        powers = {r["power"] for r in receipt["sources"]}
        self.assertEqual(len(powers), receipt["powers_added"])
        safe = {s["path"] for s in a5.safe_skills(idx)}
        for r in receipt["sources"]:
            self.assertIn(r["path"], safe)
            self.assertIn(r["power"], cov[r["path"]])
            self.assertEqual(len(r["skill_md_sha256"]), 64)

    def test_cli_unknown_id(self):
        self.assertEqual(a5.main(["show", "999999"]), 2)


if __name__ == "__main__":
    unittest.main()
