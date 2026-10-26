"""Tests for the USIP v5.8 mastery layer (A38): thinking books, GitHub pulse,
design tells and video eyes."""
import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SK = HERE.parent
SCRIPTS = SK / "scripts"


def run(script, *args):
    return subprocess.run([sys.executable, str(SCRIPTS / script), *args],
                          capture_output=True, text=True, timeout=600)


class ThinkingBooksTest(unittest.TestCase):
    def test_library_shape(self):
        data = json.loads((SK / "data/thinking_books.json").read_text())
        books = data["books"] if isinstance(data, dict) else data
        self.assertEqual(len(books), 40)
        ids = [b["id"] for b in books]
        self.assertEqual(len(ids), len(set(ids)))

    def test_self_test(self):
        r = run("thinking_books.py", "--self-test")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


class GithubPulseTest(unittest.TestCase):
    def test_snapshot_has_1000(self):
        snap = json.loads((SK / "data/github_pulse_snapshot.json").read_text())
        repos = snap["repos"] if isinstance(snap, dict) else snap
        self.assertEqual(len(repos), 1000)

    def test_generated_files_are_fresh(self):
        r = run("github_pulse.py", "build", "--check")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_self_test(self):
        r = run("github_pulse.py", "--self-test")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


class DesignTellsTest(unittest.TestCase):
    def test_self_test(self):
        r = run("design_tells.py", "--self-test")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"),
                     "ffmpeg not installed")
class VideoEyesTest(unittest.TestCase):
    def test_self_test(self):
        r = run("video_eyes.py", "--self-test")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


class AppendixTest(unittest.TestCase):
    def test_a38_is_linked_from_core(self):
        core = (SK / "PROTOCOL.md").read_text()
        self.assertIn("A38-v58-thinking-books-github-pulse.md", core)
        a38 = (SK / "references/protocol/A38-v58-thinking-books-github-pulse.md").read_text()
        for tool in ("thinking_books.py", "github_pulse.py",
                     "design_tells.py", "video_eyes.py"):
            self.assertIn(tool, a38)


if __name__ == "__main__":
    unittest.main()
