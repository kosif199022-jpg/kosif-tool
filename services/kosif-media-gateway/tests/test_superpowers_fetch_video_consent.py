"""Offline regression tests: video diagnostics never install packages implicitly."""
from __future__ import annotations

import importlib.util
import sys
import types
import unittest
from pathlib import Path
from unittest import mock

_SOURCE = Path(__file__).resolve().parents[3] / ".claude/skills/kosif-superpowers/scripts/fetch_video.py"
_spec = importlib.util.spec_from_file_location("kosif_fetch_video_install_test", _SOURCE)
video = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(video)


class FetchVideoInstallConsentTests(unittest.TestCase):
    def test_missing_dependency_is_not_installed_implicitly(self):
        deps = types.ModuleType("_deps")
        deps.ensure = mock.Mock(side_effect=AssertionError("unexpected installation"))
        with mock.patch.object(video.pinterest, "ytdlp_command", return_value=None), mock.patch.dict(sys.modules, {"_deps": deps}):
            self.assertIsNone(video.find_ytdlp())
        deps.ensure.assert_not_called()

    def test_doctor_does_not_install_dependencies(self):
        with mock.patch.object(video, "find_ytdlp", return_value=None) as find, mock.patch.object(video, "doctor", return_value=0):
            self.assertEqual(video.main(["--doctor"]), 0)
        find.assert_called_once_with(install=False)

    def test_install_deps_is_explicit_opt_in(self):
        with mock.patch.object(video, "find_ytdlp", return_value=None) as find, mock.patch.object(video, "doctor", return_value=0):
            self.assertEqual(video.main(["--doctor", "--install-deps"]), 0)
        find.assert_called_once_with(install=True)


if __name__ == "__main__":
    unittest.main()
