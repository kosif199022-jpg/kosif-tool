"""tools/job.py (background job + wait) and the no-sleep-wait PreToolUse hook."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JOB = ROOT / "tools" / "job.py"
HOOK = ROOT / ".claude" / "hooks" / "no_sleep_wait.py"


def run(*args, timeout=60):
    return subprocess.run([sys.executable, str(JOB), *args], capture_output=True, text=True, timeout=timeout)


def hook(command, background=False):
    payload = {"tool_name": "Bash", "tool_input": {"command": command, "run_in_background": background}}
    return subprocess.run([sys.executable, str(HOOK)], input=json.dumps(payload), capture_output=True, text=True, timeout=20)


class JobTest(unittest.TestCase):
    def test_success_reports_progress_and_done(self):
        with tempfile.TemporaryDirectory() as d:
            r = run("start", "--dir", d, "--", sys.executable, "-c",
                    "import time\nfor i in range(1,4):\n print(f'frame {i}/3', flush=True); time.sleep(0.3)\nprint('VERIFY OK')")
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("STARTED", r.stdout)
            w = run("wait", "--dir", d, "--every", "0", "--poll", "0.1")
            self.assertEqual(w.returncode, 0, w.stdout)
            self.assertIn("PROGRESS frame", w.stdout)
            self.assertIn("DONE exit=0", w.stdout)
            self.assertIn("DONE", run("status", "--dir", d).stdout)

    def test_failure_returns_job_exit_code_and_log_tail(self):
        with tempfile.TemporaryDirectory() as d:
            run("start", "--dir", d, "--", sys.executable, "-c", "import sys; print('Error: boom'); sys.exit(3)")
            w = run("wait", "--dir", d, "--poll", "0.1")
            self.assertEqual(w.returncode, 3)
            self.assertIn("FAILED exit=3", w.stdout)
            self.assertIn("Error: boom", w.stdout)

    def test_wait_timeout(self):
        with tempfile.TemporaryDirectory() as d:
            run("start", "--dir", d, "--", sys.executable, "-c", "import time; time.sleep(30)")
            w = run("wait", "--dir", d, "--timeout", "0.5", "--poll", "0.1")
            self.assertEqual(w.returncode, 124)
            self.assertIn("TIMEOUT", w.stdout)
            self.assertIn("STOPPED", run("stop", "--dir", d).stdout)

    def test_signal_reported_as_128_plus_signal(self):
        with tempfile.TemporaryDirectory() as d:
            run("start", "--dir", d, "--", sys.executable, "-c", "import os, signal; os.kill(os.getpid(), signal.SIGTERM)")
            w = run("wait", "--dir", d, "--poll", "0.1")
            self.assertEqual(w.returncode, 143)
            self.assertIn("FAILED exit=143", w.stdout)

    def test_missing_job(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(run("status", "--dir", d).returncode, 2)


class HookTest(unittest.TestCase):
    def test_blocks_sleep_then_check(self):
        for cmd in ('sleep 60; grep "^frame" out/render.log | tail -1',
                    "sleep 30 && tail -1 render.log",
                    "sleep 2; sleep 2; sleep 2; ls",
                    "sleep 1m; ls",
                    'python3 -c "import time; time.sleep(60)"',
                    "until test -f x; do sleep 1; done; sleep 60; cat x",
                    "for i in 1 2 3; do sleep 60; done; tail -1 render.log"):
            with self.subTest(cmd=cmd):
                r = hook(cmd)
                self.assertEqual(r.returncode, 2)
                self.assertIn("tools/job.py", r.stderr)

    def test_allows_loops_background_and_short_settle(self):
        for cmd, bg in (("until grep -q VERIFY render.log; do sleep 2; done", False),
                        ("sleep 60; grep frame render.log", True),
                        ("python3 server.py & sleep 1; curl localhost:8787", False),
                        ("echo sleep 60", False),
                        ("python3 tools/job.py status --dir out/x", False)):
            with self.subTest(cmd=cmd):
                self.assertEqual(hook(cmd, bg).returncode, 0)

    def test_hook_registered(self):
        settings = json.loads((ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))
        cmds = [h["command"] for e in settings["hooks"]["PreToolUse"] for h in e["hooks"]]
        self.assertTrue(any("no_sleep_wait.py" in c for c in cmds))


if __name__ == "__main__":
    unittest.main()
