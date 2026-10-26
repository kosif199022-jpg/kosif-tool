"""Owner-approved export standard (playbooks/export-standard.md): same or better, never lower.

Guards the shared profile and the defaults of the main delivery renderers against regressions
(a higher CRF, a faster preset, re-encoded audio, a missing +faststart).
"""
import importlib.util
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / ".claude" / "skills" / "kosif-superpowers" / "scripts"
HAVE_FFMPEG = bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))

spec = importlib.util.spec_from_file_location("export_profile", SCRIPTS / "export_profile.py")
ep = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ep)


class ProfileTests(unittest.TestCase):
    def test_standard_values(self):
        self.assertEqual((ep.WIDTH, ep.HEIGHT, ep.FPS), (1080, 1920, 30))
        self.assertLessEqual(ep.CRF, 17)
        self.assertIn(ep.PRESET, ("slow", "slower", "veryslow"))
        self.assertEqual(ep.FASTSTART, ["-movflags", "+faststart"])

    def test_video_args_never_lower_quality(self):
        args = ep.video_args(crf=23)
        self.assertEqual(args[args.index("-crf") + 1], "17")
        args = ep.video_args(crf=14)
        self.assertEqual(args[args.index("-crf") + 1], "14")
        for flag in ("bt709", "high", "yuv420p"):
            self.assertIn(flag, args)

    def test_playbook_exists_and_states_the_standard(self):
        text = (ROOT / "playbooks" / "export-standard.md").read_text(encoding="utf-8")
        for needle in ("1080×1920", "CRF 17", "+faststart", "stream-copied", "only when the user asks"):
            self.assertIn(needle, text)


class RendererDefaultsTests(unittest.TestCase):
    def test_render_html_defaults(self):
        src = (ROOT / "tools" / "render_html.cjs").read_text(encoding="utf-8")
        self.assertRegex(src, r"crf: 17\b")
        self.assertIn("'-preset', 'slow'", src)
        self.assertIn("'-c:a', 'copy'", src)
        self.assertIn("+faststart", src)
        self.assertNotIn("'192k'", src)

    def test_no_delivery_script_below_the_standard(self):
        for name in ("montage_pro.py", "fast_edit.py", "look_pipeline.py", "kosif_timeline.py", "unified_cinematic.py",
                     "blender_cinematic_bridge.py", "cinematic_broll_render.py", "unified_media.py", "creative_paint.py"):
            src = (SCRIPTS / name).read_text(encoding="utf-8")
            for crf in re.findall(r'"-crf",\s*"(\d+)"', src):
                # 28 is the 540p proxy in montage_pro, never a delivery
                self.assertTrue(int(crf) <= 17 or (name == "montage_pro.py" and crf == "28"), f"{name} uses CRF {crf}")
            self.assertFalse('"192k"' in src, f"{name} still re-encodes audio at 192k")


@unittest.skipUnless(HAVE_FFMPEG, "ffmpeg not installed")
class AudioArgsTests(unittest.TestCase):
    def test_copy_when_mp4_can_carry_it_else_aac_320(self):
        with tempfile.TemporaryDirectory() as td:
            mp3, wav = Path(td) / "v.mp3", Path(td) / "v.wav"
            for out in (mp3, wav):
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "sine=f=440:d=1", str(out)],
                               check=True, timeout=60)
            self.assertEqual(ep.audio_args(mp3), ["-c:a", "copy"])
            self.assertEqual(ep.audio_args(wav), ep.AAC_FALLBACK)
            self.assertEqual(ep.audio_args(mp3, must_reencode=True), ep.AAC_FALLBACK)


if __name__ == "__main__":
    unittest.main()
