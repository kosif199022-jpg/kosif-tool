"""v6.1 cloud edition: the ffprobe stand-in, the sandbox setup (run in a throwaway home with no ffmpeg/ffprobe on
PATH), the browser-free workbench film, and the claude.ai package limits. Nothing touches the real home folder."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
FF = shutil.which("ffmpeg")
FP = shutil.which("ffprobe")
try:
    import imageio_ffmpeg  # noqa: F401
    HAVE_IMAGEIO = True
except ImportError:
    HAVE_IMAGEIO = False


def run(cmd, env=None, cwd=None):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, cwd=cwd)


@unittest.skipUnless(FF and FP, "ffmpeg + ffprobe")
class ShimParityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="kosif_shim_"))
        cls.av = cls.tmp / "av.mp4"
        run([FF, "-y", "-v", "error", "-f", "lavfi", "-i", "testsrc2=s=320x180:r=25:d=2", "-f", "lavfi", "-i", "sine=f=440:d=2",
             "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-ac", "2", "-ar", "48000", "-shortest", str(cls.av)])

    def probe(self, tool, *args):
        cmd = [FP, *args] if tool == "real" else [sys.executable, str(SCRIPTS / "ffprobe_shim.py"), *args]
        return run(cmd).stdout

    def test_fields_the_kit_reads_match(self):
        args = ["-v", "error", "-show_entries", "stream=codec_type,codec_name,pix_fmt,width,height,r_frame_rate,nb_frames,sample_rate,channels:format=duration,size",
                "-of", "json", str(self.av)]
        real, shim = json.loads(self.probe("real", *args)), json.loads(self.probe("shim", *args))
        for r, s in zip(real["streams"], shim["streams"]):
            for k in ("codec_type", "codec_name", "width", "height", "r_frame_rate", "sample_rate", "channels"):
                self.assertEqual(r.get(k), s.get(k), k)
            if r["codec_type"] == "video":
                self.assertEqual(r["nb_frames"], s["nb_frames"])
                self.assertEqual(r["pix_fmt"], s["pix_fmt"])
        self.assertAlmostEqual(float(real["format"]["duration"]), float(shim["format"]["duration"]), delta=0.011)
        self.assertEqual(real["format"]["size"], shim["format"]["size"])

    def test_csv_and_select(self):
        self.assertAlmostEqual(float(self.probe("shim", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(self.av))), 2.0, delta=0.05)
        self.assertEqual(self.probe("shim", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", str(self.av)).strip(), "1")
        both = json.loads(self.probe("shim", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(self.av)))
        self.assertEqual(len(both["streams"]), 2); self.assertIn("duration", both["format"])
        self.assertNotEqual(run([sys.executable, str(SCRIPTS / "ffprobe_shim.py"), "-v", "error", str(self.tmp / "missing.mp4")]).returncode, 0)


@unittest.skipUnless(HAVE_IMAGEIO, "imageio-ffmpeg")
class SandboxSetupTests(unittest.TestCase):
    """A sandbox with no ffmpeg or ffprobe on PATH and a throwaway home: setup, then a browser-free film through kmotion."""

    def test_setup_then_workbench(self):
        tmp = Path(tempfile.mkdtemp(prefix="kosif_cloud_"))
        home = tmp / "userhome"; home.mkdir()
        clean = os.pathsep.join(p for p in os.environ["PATH"].split(os.pathsep)
                                if not (Path(p) / ("ffmpeg.exe" if os.name == "nt" else "ffmpeg")).exists()
                                and not (Path(p) / ("ffprobe.exe" if os.name == "nt" else "ffprobe")).exists())
        env = {**os.environ, "PATH": clean, "HOME": str(home), "USERPROFILE": str(home), "PYTHONUTF8": "1"}
        env.pop("KOSIF_MOTION_HOME", None)
        r = run([sys.executable, str(SCRIPTS / "kmotion.py"), "setup"], env=env)
        self.assertEqual(r.returncode, 0, r.stderr[-800:])
        rep = json.loads(r.stdout[r.stdout.find("{"): r.stdout.rfind("}") + 1])
        self.assertTrue(rep["ffmpeg"]["path"]); self.assertIn("stand-in", rep["ffprobe"]["source"])
        self.assertTrue((home / ".kosif-motion.json").exists())
        self.assertIn("midnight_cat", rep["examples_copied"])
        out = home / "kosif-motion" / "out" / "wb.mp4"
        r = run([sys.executable, str(SCRIPTS / "kmotion.py"), "workbench", "اختبار سحابي", "--aspect", "9:16", "--seconds", "2", "--fps", "24",
                 "--titles", "أ|ب|ج|د|هـ", "--out", str(out)], env=env)
        self.assertEqual(r.returncode, 0, r.stderr[-800:])
        meta = json.loads(r.stdout[r.stdout.find("{"):])
        self.assertEqual((meta["width"], meta["height"], meta["frames"]), (1080, 1920, 48))
        r2 = run([sys.executable, str(SCRIPTS / "kmotion.py"), "setup"], env=env)                 # a re-run rewrites, never adopts, its own bin
        rep2 = json.loads(r2.stdout[r2.stdout.find("{"): r2.stdout.rfind("}") + 1])
        self.assertIn("stand-in", rep2["ffprobe"]["source"])
        shutil.rmtree(tmp, ignore_errors=True)


class PackageLimitTests(unittest.TestCase):
    def test_claude_ai_package_fits(self):
        out = Path(tempfile.mkdtemp(prefix="kosif_pkg_")) / "up.zip"
        r = run([sys.executable, str(SCRIPTS / "build_package.py"), "--claude-ai", "--out", str(out)])
        self.assertEqual(r.returncode, 0, r.stderr[-500:])
        z = zipfile.ZipFile(out)
        self.assertLessEqual(len(z.namelist()), 200)
        self.assertIn("kosif-montage-motion/SKILL.md", z.namelist())
        self.assertIn("kosif-montage-motion/scripts/cloud_setup.py", z.namelist())
        self.assertIn("kosif-montage-motion/scripts/ffprobe_shim.py", z.namelist())
        import yaml
        text = z.read("kosif-montage-motion/SKILL.md").decode("utf-8").replace("\r\n", "\n")
        self.assertTrue(text.startswith("---\nname:"), "SKILL.md must start with LF YAML front matter")
        head = text.split("\n---\n", 1)[0].strip("-\n")
        d = yaml.safe_load(head)
        self.assertLessEqual(len(d["description"]), 1024); self.assertRegex(d["name"], r"^[a-z0-9-]{1,64}$")


if __name__ == "__main__":
    unittest.main()
