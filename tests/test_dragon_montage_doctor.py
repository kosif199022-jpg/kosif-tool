"""Dragon Montage Phase 0: the tools manifest and dm_doctor.py (fast, no network)."""
import json
import re
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".claude" / "skills" / "kosif-dragon-montage"
SCRIPTS = SKILL / "scripts"
MANIFEST = SKILL / "data" / "required_tools.json"
DOCTOR = SCRIPTS / "dm_doctor.py"
STATIONS = {"analyze", "think", "taste", "direct", "render", "review", "generate"}
TIERS = {"required", "recommended", "optional"}
CHECK_KINDS = {"bin", "py", "node", "browser", "font", "python"}

sys.path.insert(0, str(SCRIPTS))
import dm_doctor  # noqa: E402


def run(*args):
    return subprocess.run([sys.executable, str(DOCTOR), *args], capture_output=True, text=True,
                          encoding="utf-8", timeout=120)


class ManifestSchema(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_top_level(self):
        self.assertEqual(self.m["schema"], "kosif.dm.required_tools.v1")
        self.assertEqual(set(self.m["stations"]), STATIONS)
        self.assertTrue(self.m["tools"])
        self.assertTrue(self.m["services"])

    def test_every_tool_is_complete(self):
        ids = [t["id"] for t in self.m["tools"]]
        self.assertEqual(len(ids), len(set(ids)), "duplicate tool ids")
        for t in self.m["tools"]:
            with self.subTest(tool=t["id"]):
                for k in ("id", "name", "tier", "purpose", "stations", "check", "install", "size", "breaks_without"):
                    self.assertIn(k, t)
                self.assertIn(t["tier"], TIERS)
                self.assertTrue(t["purpose"]["ar"].strip() and t["purpose"]["en"].strip())
                self.assertTrue(set(t["stations"]) <= STATIONS and t["stations"])
                self.assertTrue(t["check"])
                for c in t["check"]:
                    self.assertIn(c["kind"], CHECK_KINDS)
                for dep in t.get("needs", []):
                    self.assertIn(dep, ids)
                ins = t["install"]
                self.assertTrue(set(ins) <= {"pip", "npm", "linux", "macos", "windows", "ashell", "post"})
                has_any = ins.get("pip") or ins.get("npm") or ins.get("post") or any(
                    ins.get(o) for o in ("linux", "macos", "windows"))
                self.assertTrue(has_any, "no install route")

    def test_every_station_has_a_required_tool(self):
        for s in STATIONS:
            with self.subTest(station=s):
                self.assertTrue([t for t in self.m["tools"] if t["tier"] == "required" and s in t["stations"]])

    def test_core_tools_are_required(self):
        tiers = {t["id"]: t["tier"] for t in self.m["tools"]}
        for core in ("python", "ffmpeg", "ffprobe"):
            self.assertEqual(tiers[core], "required")

    def test_services_are_keys_not_installs(self):
        for s in self.m["services"]:
            with self.subTest(service=s["id"]):
                self.assertNotIn("install", s)
                self.assertTrue(s["env"] or s.get("connector"))
                for e in s["env"]:
                    self.assertRegex(e, r"^[A-Z][A-Z0-9_]+$")
        ids = {s["id"] for s in self.m["services"]}
        self.assertTrue({"kling", "higgsfield", "suno", "gemini"} <= ids)

    def test_requirements_file_covers_required_and_recommended_pip(self):
        req = (SKILL / "requirements-montage.txt").read_text(encoding="utf-8")
        active = {re.split(r"[<>=\s]", l.strip())[0].lower() for l in req.splitlines()
                  if l.strip() and not l.lstrip().startswith("#")}
        for t in self.m["tools"]:
            if t["tier"] in ("required", "recommended"):
                for p in t["install"].get("pip", []):
                    self.assertIn(re.split(r"[<>=\[]", p)[0].lower(), active, t["id"])


class Doctor(unittest.TestCase):
    @unittest.skipUnless(shutil.which("ffmpeg"), "ffmpeg not on PATH")
    def test_doctor_json_reports_ffmpeg(self):
        r = run("doctor", "--json")
        rep = json.loads(r.stdout)
        self.assertEqual(rep["schema"], "kosif.dm.doctor.v1")
        ff = next(t for t in rep["tools"] if t["id"] == "ffmpeg")
        self.assertTrue(ff["present"])
        self.assertEqual(set(rep["stations"]), STATIONS)
        self.assertEqual(r.returncode, 0 if rep["ready"] else 1)
        if not rep["missing_required"]:
            self.assertEqual(r.returncode, 0)

    def test_tier_filter(self):
        rep = json.loads(run("doctor", "--json", "--tier", "required").stdout)
        self.assertEqual({t["tier"] for t in rep["tools"]}, {"required"})
        self.assertEqual(set(rep["stations"]), STATIONS)

    def test_human_report_is_arabic(self):
        out = run("doctor").stdout
        self.assertIn("الحكم", out)
        self.assertIn("العين الأولى", out)

    def test_missing_required_makes_station_not_ready(self):
        m = json.loads(MANIFEST.read_text(encoding="utf-8"))
        m["tools"].append({"id": "ghost", "name": "Ghost", "tier": "required", "stations": ["think"],
                           "purpose": {"ar": "x", "en": "x"}, "check": [{"kind": "bin", "name": "no-such-tool-xyz"}],
                           "install": {"pip": ["ghost"]}, "size": "0", "breaks_without": "x"})
        rep = dm_doctor.check_all("all", m)
        self.assertFalse(rep["ready"])
        self.assertIn("ghost", rep["missing_required"])
        self.assertEqual(rep["stations"]["think"]["level"], "not-ready")


class InstallPlan(unittest.TestCase):
    EXPECT = {"linux": "apt-get install", "macos": "brew install", "windows": "winget install"}

    def test_plan_for_each_os(self):
        for os_name, needle in self.EXPECT.items():
            with self.subTest(os=os_name):
                r = run("install-plan", "--os", os_name, "--all", "--tier", "all")
                self.assertEqual(r.returncode, 0, r.stderr)
                self.assertIn(needle, r.stdout)
                self.assertIn("ffmpeg" if os_name != "windows" else "Gyan.FFmpeg", r.stdout)
                self.assertRegex(r.stdout, r"(python3|py) -m pip install")

    def test_ashell_plan(self):
        r = run("install-plan", "--os", "ashell", "--all", "--tier", "recommended")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("pip install --upgrade yt-dlp", r.stdout)

    def test_cpu_torch_before_demucs(self):
        lines = dm_doctor.install_plan("linux", "all", everything=True)
        torch = next(i for i, l in enumerate(lines) if "download.pytorch.org/whl/cpu" in l)
        demucs = next(i for i, l in enumerate(lines) if "demucs" in l and "pip install" in l)
        self.assertLess(torch, demucs)

    def test_missing_only_is_subset(self):
        full = set(dm_doctor.install_plan("linux", "all", everything=True))
        missing = [l for l in dm_doctor.install_plan("linux", "all") if not l.startswith("#")]
        self.assertTrue(all(l in full or "pip install" in l or "apt-get" in l or "npm install" in l for l in missing))

    def test_install_scripts_exist_and_never_called_by_doctor(self):
        for f in ("install_tools.sh", "install_tools.ps1"):
            self.assertTrue((SCRIPTS / f).is_file())
        src = DOCTOR.read_text(encoding="utf-8")
        self.assertNotIn("pip install", re.sub(r'["\'].*?["\']', "", src))  # only in strings

    @unittest.skipUnless(shutil.which("bash"), "bash missing")
    def test_install_sh_syntax(self):
        r = subprocess.run(["bash", "-n", str(SCRIPTS / "install_tools.sh")], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)


if __name__ == "__main__":
    unittest.main()
