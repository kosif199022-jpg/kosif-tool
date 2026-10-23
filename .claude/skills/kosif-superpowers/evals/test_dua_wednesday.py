"""«دعاء يوم الأربعاء» engine: timeline maths always; a real 2-second render on synthetic media when ffmpeg,
numpy, OpenCV and Node+Playwright are present (skipped otherwise)."""
import json, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path
SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK / "scripts"))
import dua_wednesday as D  # noqa: E402


def _have_render_stack():
    if not (shutil.which("ffmpeg") and shutil.which("node")):
        return False
    try:
        import cv2, numpy  # noqa: F401
    except ImportError:
        return False
    return subprocess.run(["node", "-e", "require(process.argv[1])", "/opt/node-tools/node_modules/playwright"],
                          capture_output=True).returncode == 0


class TimelineTests(unittest.TestCase):
    def test_example_project_timeline(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            shutil.copy(D.PKG / "project.example.json", tmp / "project.json")
            p = D.load_project(tmp)
            self.assertEqual(len(p["lines"]), 10)
            self.assertEqual(len(p["transitions"]), 9)
            self.assertEqual(len(set(p["transitions"])), 9, "every cut uses a different transition")
            self.assertEqual(p["cuts"][0], 0.0)
            for c, line in zip(p["cuts"][1:], p["lines"][1:]):
                self.assertAlmostEqual(c, line[0][1] - 0.24, places=6)      # cut just before the voice onset
            for i, d in enumerate(p["tdur"]):                                # transitions fit inside both shots
                self.assertLess(d, p["cuts"][i + 1] - p["cuts"][i])
            self.assertEqual(p["title"], "الأربعاء")
            spec = D.sprite_spec(p)
            ids = {it["id"] for it in spec["items"]}
            self.assertTrue({"title", "date", "sub", "L0w", "L0g", "L9w"} <= ids)
            for f in spec["fonts"].values():
                self.assertTrue(Path(f).exists(), f)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_no_star_ornament(self):
        src = (SK / "scripts" / "dua_wednesday.py").read_text(encoding="utf-8")
        self.assertIn("def draw_mihrab", src)
        self.assertNotIn("draw_ornament", src)           # the owner rejected the star; mihrab + crescent only


class StructuredErrorTests(unittest.TestCase):
    """Bad input or a missing optional module gives one JSON line and exit 2, never a traceback."""

    def _cli(self, *args):
        r = subprocess.run([sys.executable, str(SK / "scripts" / "dua_wednesday.py"), *args],
                           capture_output=True, text=True, timeout=60)
        self.assertNotIn("Traceback", r.stderr + r.stdout)
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
        return json.loads(r.stdout.strip().splitlines()[-1])

    def test_caption_times_missing_file(self):
        out = self._cli("caption-times", "/nonexistent/clip.mp4")
        self.assertIn(out["status"], ("error", "missing_requirements"))
        self.assertEqual(out["cmd"], "caption-times")

    @unittest.skipUnless(shutil.which("ffprobe") and shutil.which("ffmpeg"), "ffprobe/ffmpeg missing")
    def test_caption_times_not_a_video(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            (tmp / "x.mp4").write_text("not a video")
            out = self._cli("caption-times", str(tmp / "x.mp4"))
            self.assertIn(out["status"], ("error", "missing_requirements"))
            if out["status"] == "error":
                self.assertIn("no readable video stream", out["error"])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_prep_missing_clip(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            out = self._cli("prep", "--job", str(tmp / "job"), str(tmp / "missing.mp4"))
            if out["status"] == "error":
                self.assertEqual(out["missing"], [str(tmp / "missing.mp4")])
                self.assertFalse((tmp / "job").exists(), "nothing is written before validation")
            else:
                self.assertEqual(out["status"], "missing_requirements")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_asr_and_stills_report_missing_modules(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            for cmd, mods in (("asr", ("numpy", "faster_whisper")), ("stills", ("numpy", "cv2"))):
                with self.subTest(cmd=cmd):
                    args = [cmd, "--job", str(tmp)] + (["--t", "1"] if cmd == "stills" else [])
                    out = self._cli(*args)
                    self.assertEqual(out["cmd"], cmd)
                    if out["status"] == "missing_requirements":
                        self.assertTrue(set(out["missing"]) <= set(mods) | {"ffmpeg"}, out)
                    else:            # every module present: the missing job input is reported instead
                        self.assertEqual(out["status"], "error")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_require_helper(self):
        with self.assertRaises(D.CommandError) as cm:
            D.require("x", modules=("definitely_not_a_module_kosif",), tools=("definitely-not-a-binary-kosif",))
        self.assertEqual(cm.exception.payload, {"cmd": "x", "status": "missing_requirements",
                                                "missing": ["definitely_not_a_module_kosif", "definitely-not-a-binary-kosif"]})


@unittest.skipUnless(_have_render_stack(), "ffmpeg / numpy / OpenCV / Node+Playwright not all installed")
class RenderTests(unittest.TestCase):
    def test_two_line_render_keeps_audio(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            for name, src in (("a.mp4", "testsrc2"), ("b.mp4", "smptebars")):
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"{src}=size=640x360:rate=30:duration=3",
                                "-c:v", "libx264", "-pix_fmt", "yuv420p", str(tmp / name)], check=True)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "sine=frequency=220:duration=2",
                            "-c:a", "aac", "-b:a", "128k", str(tmp / "voice.m4a")], check=True)
            self.assertEqual(D.main(["prep", "--job", str(tmp), str(tmp / "a.mp4"), str(tmp / "b.mp4") + ":100", "--seconds", "3"]), 0)
            (tmp / "project.json").write_text(json.dumps({
                "audio": "voice.m4a", "duration": 2.0, "title": "الأربعاء", "date_line": "21.10.2026",
                "lines": [[["اللَّهُمَّ", 0.1], ["آمين", 0.5]], [["يا", 1.1], ["رب", 1.3]]],
                "shots": [{"clip": "v/00.mp4"}, {"clip": "v/01.mp4"}], "transitions": ["ink_reveal"]}, ensure_ascii=False),
                encoding="utf-8")
            self.assertEqual(D.main(["sprites", "--job", str(tmp)]), 0)
            self.assertEqual(D.main(["render", "--job", str(tmp), "--workers", "2"]), 0)
            rep = json.loads((tmp / "out" / "report.json").read_text())
            self.assertEqual(rep["frames"], 60)
            self.assertTrue(rep["audio_untouched"])
            self.assertTrue((tmp / "out" / "tiktok.mp4").exists())
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
