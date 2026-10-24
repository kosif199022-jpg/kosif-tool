"""Download dependencies: cloud auto-install, a never-failing report, and an honest message when a site blocks the cloud."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / ".claude" / "skills" / "kosif-superpowers" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import _deps  # noqa: E402
import fetch_video  # noqa: E402


class DepsTest(unittest.TestCase):
    def test_autoinstall_only_in_cloud_sessions(self):
        with mock.patch.dict(os.environ, {"CLAUDE_CODE_REMOTE": "true"}, clear=False):
            os.environ.pop("KOSIF_NO_AUTOINSTALL", None)
            self.assertTrue(_deps.autoinstall_allowed())
        with mock.patch.dict(os.environ, {"CLAUDE_CODE_REMOTE": "true", "KOSIF_NO_AUTOINSTALL": "1"}):
            self.assertFalse(_deps.autoinstall_allowed())
        env = {k: v for k, v in os.environ.items() if k not in ("CLAUDE_CODE_REMOTE", "KOSIF_AUTOINSTALL", "KOSIF_NO_AUTOINSTALL")}
        with mock.patch.dict(os.environ, env, clear=True):
            self.assertFalse(_deps.autoinstall_allowed())

    def test_ensure_does_not_install_when_not_allowed(self):
        with mock.patch.object(_deps, "autoinstall_allowed", return_value=False), mock.patch.object(_deps, "pip_install") as pip:
            self.assertEqual(_deps.ensure(["surely_not_a_module_kosif"]), ["surely_not_a_module_kosif"])
            pip.assert_not_called()

    def test_report_never_fails(self):
        p = subprocess.run([sys.executable, str(SCRIPTS / "_deps.py")], capture_output=True, text=True, timeout=60)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("yt-dlp", p.stdout)

    def test_block_detection(self):
        for err in ("ERROR: [TikTok] 123: Your IP address is blocked from accessing this post",
                    "ERROR: [youtube] x: Sign in to confirm you're not a bot",
                    "ERROR: unable to download webpage: HTTP Error 403: Forbidden"):
            self.assertTrue(_deps.is_blocked(err), err)
        self.assertFalse(_deps.is_blocked("ERROR: Unsupported URL: https://example.com"))
        hint = _deps.blocked_hint("https://vt.tiktok.com/abc/")
        self.assertIn("tiktok", hint)
        self.assertIn("--cookies-from-browser", hint)
        self.assertIn("upload", hint)

    def test_fetch_video_marks_blocked_download(self):
        a = mock.Mock(out=str(ROOT / "out" / "_test_dl"), quality="1080", cookies=None, connections=1, proxy=None,
                      safe=False, cookies_from_browser=None)
        with mock.patch.object(fetch_video, "impersonation", return_value=None), \
             mock.patch.object(fetch_video, "attempt", return_value=(None, "ERROR: [TikTok] Your IP address is blocked")):
            rec = fetch_video.download("https://www.tiktok.com/@a/video/1", a, ["yt-dlp"])
        self.assertIsNone(rec["file"])
        self.assertTrue(rec["blocked"])
        self.assertIn("--cookies-from-browser", rec["hint"])

    def test_boot_reports_download_tools_and_exits_zero(self):
        env = {**os.environ, "KOSIF_NO_AUTOINSTALL": "1"}
        p = subprocess.run([sys.executable, str(SCRIPTS / "boot.py"), "--json"], capture_output=True, text=True, timeout=120, env=env)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("download_tools", json.loads(p.stdout))

    def test_session_start_hook_is_registered_and_never_fails(self):
        settings = json.loads((ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))
        cmds = [h["command"] for g in settings["hooks"]["SessionStart"] for h in g["hooks"]]
        self.assertTrue(any("session-start.sh" in c for c in cmds))
        hook = ROOT / ".claude" / "hooks" / "session-start.sh"
        self.assertTrue(os.access(hook, os.X_OK))
        env = {k: v for k, v in os.environ.items() if k not in ("CLAUDE_CODE_REMOTE", "KOSIF_AUTOINSTALL")}
        self.assertEqual(subprocess.run(["bash", str(hook)], env=env, timeout=30).returncode, 0)


if __name__ == "__main__":
    unittest.main()
