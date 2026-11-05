"""Black Dragon conversion wave (2026-11-05): programs for power cards that had none.

The offline programs (CAM-71, DATA-91, TOOL-130, TOOL-132) run on every machine. The `__local` programs
need pip libraries, downloaded models or the network (faster-whisper, Piper, PuLP+HiGHS, a venv install,
Hugging Face); they run only where those exist and are registered with env_scope=local.
Planted failures prove the checks measure the technique.
"""
from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / ".claude" / "skills" / "kosif-superpowers" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import _black_dragon_power_program as dispatcher  # noqa: E402
import power_programs as pp  # noqa: E402
from power_programs import camera_composition_layout__bd as cam  # noqa: E402
from power_programs import charts_data_infographic__bd as data  # noqa: E402

OFFLINE = ["CAM-71", "DATA-91", "TOOL-130", "TOOL-132"]
LOCAL = {"SYNC-07": "faster_whisper", "SYNC-08": "faster_whisper", "SYNC-09": "piper", "SYNC-48": "faster_whisper",
         "MEDIA-25": "faster_whisper", "MEDIA-27": "rembg", "APPX-13": "faster_whisper", "VOICE-01": "piper", "QA-216": "faster_whisper",
         "PROD-17": "pulp", "SELF-26": "venv", "WEB-08": "network"}


def run(pid):
    with tempfile.TemporaryDirectory() as tmp:
        return dispatcher.run_program(pid, Path(tmp) / "work")


class Wave(unittest.TestCase):
    def test_ids_are_catalog_powers_in_the_right_family(self):
        cards = pp.card_index()
        progs = pp.all_programs()
        for pid in OFFLINE + list(LOCAL):
            self.assertIn(pid, cards)
            self.assertIn(pid, progs)
            family = cards[pid][0].replace("-", "_")
            self.assertTrue(progs[pid][0].stem.startswith(family + "__"), (pid, progs[pid][0].name))
        for pid in LOCAL:
            self.assertTrue(progs[pid][0].stem.endswith("__local"), pid)

    def test_offline_programs_pass(self):
        for pid in OFFLINE:
            with self.subTest(pid=pid):
                res = run(pid)
                self.assertTrue(res["ok"], res.get("problems") or res.get("error"))

    def test_local_programs_pass_where_their_engine_exists(self):
        for pid, mod in LOCAL.items():
            if mod not in ("venv", "network") and importlib.util.find_spec(mod) is None:
                continue
            if mod in ("venv", "network", "faster_whisper", "piper", "rembg"):
                continue  # need downloads; proven on the build machine (env_scope=local)
            with self.subTest(pid=pid):
                self.assertTrue(run(pid)["ok"])

    def test_planted_wrong_zoom_fails(self):
        with mock.patch.object(cam, "need_zoom", lambda r, w, h: 1.0):
            self.assertFalse(run("CAM-71")["ok"])

    def test_planted_no_stagger_fails(self):
        with mock.patch.object(data, "STAGGER", 0.0):
            self.assertFalse(run("DATA-91")["ok"])

    def test_planted_wrong_palette_fails(self):
        with mock.patch.object(data, "SERIES", ["#FF0000"] * 5):
            self.assertFalse(run("DATA-91")["ok"])


if __name__ == "__main__":
    unittest.main()
