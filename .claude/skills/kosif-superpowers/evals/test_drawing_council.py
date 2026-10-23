import json
import subprocess
import sys
import tempfile
import unittest
import zlib
import struct
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK / "scripts"))
import drawing_council as dc  # noqa: E402
import drawing_methods as dm  # noqa: E402

SCRIPT = SK / "scripts" / "drawing_council.py"
SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" data-floating="ground">
<rect id="ground" data-part="ground" x="0" y="180" width="200" height="20"/>
<g data-figure="man"><circle data-part="head" cx="100" cy="60" r="20"/>
<rect data-part="body" x="85" y="{body_y}" width="30" height="60"/>
<rect data-part="foot" data-contact="ground" x="85" y="140" width="30" height="40"/></g></svg>"""


def png(path, shade=200):
    raw = b"".join(b"\x00" + bytes([shade, shade, shade]) * 4 for _ in range(4))
    chunk = lambda t, d: struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", 4, 4, 8, 2, 0, 0, 0))
                     + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))


def answer(eid, verdict="pass", beauty=4, fix=True):
    a = {"expert": eid, "verdict": verdict, "scores": {"correctness": 4, "craft": 4, "beauty": beauty},
         "findings": [], "evidence": ["opened the PNG"]}
    if verdict != "pass":
        a["findings"] = [{"check": "DM-08", "observed": "waist gap",
                          **({"fix": "join hips to chest", "code": {"where": "s.svg:3 man/hips", "cause": "y=95 leaves a gap",
                                                                    "change": "y=80"}} if fix else {})}]
    return a


class RosterTests(unittest.TestCase):
    def test_every_card_belongs_to_exactly_one_expert(self):
        ids = [c for e in dc.EXPERTS for c in e["cards"]]
        atlas = {m["id"] for m in dm.load_atlas()["methods"]}
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(set(ids), atlas)
        self.assertEqual(len(dc.EXPERTS), 11)

    def test_roster_expands_cards_and_books(self):
        for e in dc.roster():
            self.assertTrue(e["veto"] and e["books"] and e["methods"], e["id"])
            for m in e["methods"]:
                self.assertTrue(m["checks"] and m["common_errors"], m["id"])

    def test_persona_file_is_current_and_in_council_schema(self):
        stored = json.loads((SK / "data" / "drawing_council_personas.json").read_text(encoding="utf-8"))
        self.assertEqual(stored, dc.personas(dc.roster()))
        self.assertEqual(stored["schema"], "kosif.council-personas.v1")
        lanes = {"cross_domain", "verification", "feasibility", "audience", "guardrails"}
        for p in stored["personas"]:
            self.assertRegex(p["id"], r"^D\d\d$")
            self.assertIn(p["lane"], lanes)
            self.assertEqual(len(p["superpowers"]), 3)
            self.assertEqual(len(p["signature_questions"]), 3)


class FlowTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.t = Path(self.tmp.name)
        png(self.t / "s.png")

    def tearDown(self):
        self.tmp.cleanup()

    def plan(self, body_y=80, name="c", extra=()):
        (self.t / "s.svg").write_text(SVG.format(body_y=body_y), encoding="utf-8")
        d = self.t / name
        r = subprocess.run([sys.executable, str(SCRIPT), "plan", "--png", str(self.t / "s.png"), "--svg", str(self.t / "s.svg"),
                            "--brief", "رجل واقف", "--dir", str(d), *extra], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        return d

    def ingest(self, d, a, simulated=False):
        f = self.t / f"{a['expert']}.json"
        f.write_text(json.dumps(a), encoding="utf-8")
        args = [sys.executable, str(SCRIPT), "ingest", "--dir", str(d), "--expert", a["expert"], "--file", str(f)]
        return subprocess.run(args + (["--simulated"] if simulated else []), capture_output=True, text=True)

    def test_plan_writes_a_prompt_per_expert_with_cards_and_vetoes(self):
        d = self.plan()
        prompts = sorted((d / "prompts").glob("E*.md"))
        self.assertEqual(len(prompts), 11)
        e04 = (d / "prompts" / "E04.md").read_text(encoding="utf-8")
        self.assertIn("DM-12", e04)
        self.assertIn("Veto conditions", e04)
        self.assertIn('"status": "PASS"', e04)

    def test_all_experts_pass_gives_pass_and_simulated_is_labelled(self):
        d = self.plan()
        for e in dc.EXPERTS:
            self.assertEqual(self.ingest(d, answer(e["id"]), simulated=e["id"] == "E07").returncode, 0)
        v = dc.verdict(d)
        self.assertEqual(v["status"], "PASS", v["reasons"])
        self.assertEqual(v["mode"], "SIMULATED")
        self.assertEqual(v["simulated_experts"], ["E07"])

    def test_veto_low_beauty_and_missing_experts_block(self):
        d = self.plan()
        for e in dc.EXPERTS[:-1]:
            self.ingest(d, answer(e["id"], beauty=3))
        self.assertEqual(dc.verdict(d)["status"], "INCOMPLETE")
        self.ingest(d, answer("E11", verdict="veto"))
        v = dc.verdict(d)
        self.assertEqual(v["status"], "FAIL")
        self.assertTrue(any("veto" in r for r in v["reasons"]))
        self.assertTrue(any("mean beauty" in r for r in v["reasons"]))
        self.assertEqual(v["required_fixes"][0]["fix"], "join hips to chest")
        r = subprocess.run([sys.executable, str(SCRIPT), "verdict", "--dir", str(d)], capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)
        self.assertIn("التصليحات المطلوبة", (d / "minutes.md").read_text(encoding="utf-8"))

    def test_detached_body_fails_even_when_every_expert_passes(self):
        d = self.plan(body_y=95)  # head ends at 80: a 15px gap at the neck
        for e in dc.EXPERTS:
            self.ingest(d, answer(e["id"]))
        v = dc.verdict(d)
        self.assertEqual(v["status"], "FAIL")
        self.assertEqual(v["automated"]["law27_review"], "FAIL")

    def test_a_changed_image_invalidates_the_council(self):
        d = self.plan()
        for e in dc.EXPERTS:
            self.ingest(d, answer(e["id"]))
        png(self.t / "s.png", shade=10)
        self.assertTrue(any("PNG changed" in r for r in dc.verdict(d)["reasons"]))

    def test_ingest_rejects_a_fix_without_a_fix_and_unknown_experts(self):
        d = self.plan()
        r = self.ingest(d, answer("E02", verdict="fix", fix=False))
        self.assertEqual(r.returncode, 2)
        self.assertIn("concrete fix", r.stderr)
        r = self.ingest(d, dict(answer("E02"), expert="E99"))
        self.assertEqual(r.returncode, 2)

    def test_fixes_must_name_the_code_that_causes_them(self):
        d = self.plan()
        prompt = (d / "prompts" / "E02.md").read_text(encoding="utf-8")
        self.assertIn("name the cause, not only the symptom", prompt)
        self.assertIn("· man · body ·", prompt)
        a = answer("E02", verdict="fix")
        del a["findings"][0]["code"]
        r = self.ingest(d, a)
        self.assertEqual(r.returncode, 2)
        self.assertIn("code.where", r.stderr)
        self.assertEqual(self.ingest(d, answer("E02", verdict="fix")).returncode, 0)
        dc.cmd_verdict(type("A", (), {"dir": str(d)})())
        self.assertIn("الكود: `s.svg:3 man/hips`", (d / "minutes.md").read_text(encoding="utf-8"))

    def test_style_lock_and_a_worse_round_than_the_baseline_fails(self):
        png(self.t / "base.png", shade=120)
        d = self.plan(extra=["--style", "flat cartoon, bold outlines", "--baseline", str(self.t / "base.png")])
        prompt = (d / "prompts" / "E06.md").read_text(encoding="utf-8")
        self.assertIn("Style lock", prompt)
        self.assertIn("vs_baseline", prompt)
        r = self.ingest(d, answer("E01"))
        self.assertEqual(r.returncode, 2)
        self.assertIn("vs_baseline", r.stderr)
        for i, e in enumerate(dc.EXPERTS):
            self.ingest(d, dict(answer(e["id"]), vs_baseline="worse" if i < 6 else "better"))
        v = dc.verdict(d)
        self.assertEqual(v["status"], "FAIL")
        self.assertTrue(any("worse than the baseline" in r for r in v["reasons"]))

    def test_protocol_requires_the_council(self):
        core = (SK / "PROTOCOL.md").read_text(encoding="utf-8")
        self.assertIn("A31-drawing-council.md", core)
        self.assertIn("drawing_council.py", core.split("\n27. ", 1)[1].split("\n", 1)[0])
        self.assertIn("A31-drawing-council.md", (SK / "USIP_PORTABLE.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
