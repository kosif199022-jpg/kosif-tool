"""Tests for Black Dragon's real media runner and fail-closed evidence contract."""
from __future__ import annotations

import argparse
import json
import math
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
import wave
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / ".claude" / "skills" / "kosif-superpowers" / "scripts"
sys.path.insert(0, str(SCRIPTS))
import black_dragon_media as media  # noqa: E402


def wav_fixture(path: Path, duration=2.0, rate=8000):
    with wave.open(str(path), "wb") as stream:
        stream.setnchannels(1)
        stream.setsampwidth(2)
        stream.setframerate(rate)
        values = []
        for n in range(round(duration * rate)):
            # A regular sound with deliberate amplitude transients.
            loud = 0.65 if int(n / (rate * 0.35)) % 2 else 0.08
            values.append(int(32767 * loud * math.sin(2 * math.pi * 330 * n / rate)))
        stream.writeframes(struct.pack("<" + "h" * len(values), *values))


class MediaContractTests(unittest.TestCase):
    def test_path_validation_rejects_traversal_and_links(self):
        for name in ("../oops", "bad/name", "contains space", "", "é"):
            with self.assertRaises(ValueError, msg=name):
                media.job_path(name)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            src = root / "ok.wav"
            wav_fixture(src, duration=0.2)
            self.assertEqual(media.existing_file(src), src.resolve())
            (root / "link.wav").symlink_to(src)
            with self.assertRaises(ValueError):
                media.existing_file(root / "link.wav")

    def test_explicit_execution_consent_required_and_no_job_created(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "audio.wav"
            wav_fixture(source, duration=0.2)
            args = argparse.Namespace(input=source, aligned_words=None, job_name="never-run",
                                      execute=False, timeout=60, skip_scenes=True,
                                      stabilize=False, reframe=False, grade_look=None)
            with mock.patch.object(media, "JOBS", root / "jobs"):
                with self.assertRaisesRegex(ValueError, "--execute"):
                    media.run(args)
                self.assertFalse((root / "jobs").exists())

    def test_verify_rejects_tampering_and_symlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with mock.patch.object(media, "JOBS", root / "jobs"):
                job = media.job_path("proof")
                job.mkdir(parents=True)
                output = job / "result.json"
                output.write_text('{"real":true}\n')
                proof = media.artifact_proof(job, output)
                report = {"schema": media.SCHEMA, "status": "completed",
                          "verified_artifact_count": 1,
                          "stages": [{"name": "test", "status": "executed", "artifacts": [proof]}]}
                media._save(job, report)
                self.assertEqual(media.verify("proof")["verified_artifacts"], 1)
                output.write_text('{"real":false}\n')
                with self.assertRaisesRegex(ValueError, "artifact changed"):
                    media.verify("proof")
                output.unlink()
                outside = root / "outside"
                outside.write_text("not an artifact")
                output.symlink_to(outside)
                with self.assertRaises(ValueError):
                    media.verify("proof")

    def test_main_black_dragon_cli_routes_media_doctor(self):
        result = subprocess.run([sys.executable, str(SCRIPTS / "black_dragon.py"),
                                 "media", "doctor"], capture_output=True, text=True, timeout=90)
        self.assertEqual(result.returncode, 0, result.stderr[-500:])
        data = json.loads(result.stdout)
        self.assertEqual(data["schema"], media.SCHEMA + ".doctor")
        self.assertIn("ffmpeg", data)

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"),
                         "ffmpeg and ffprobe are required for real media integration")
    def test_real_audio_intake_and_rhythm_create_verified_outputs(self):
        if not all((SCRIPTS / x).is_file() for x in media.TOOLS.values()):
            self.skipTest("Bundled media tools unavailable")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "original.wav"
            wav_fixture(source)
            before = media.digest(source)
            args = argparse.Namespace(input=source, aligned_words=None, job_name="audio-test",
                                      execute=True, timeout=180, skip_scenes=True,
                                      stabilize=False, reframe=False, grade_look=None)
            with mock.patch.object(media, "JOBS", root / "jobs"):
                status, report = media.run(args)
                self.assertEqual(status, 0, report.get("error"))
                self.assertEqual(report["status"], "completed")
                self.assertEqual(report["media_kind"], "audio")
                self.assertFalse(report["catalog_coverage_claim"])
                self.assertEqual(report["paid_provider_calls"], 0)
                self.assertTrue((root / "jobs" / "audio-test" / "rhythm.json").is_file())
                result = json.loads((root / "jobs" / "audio-test" / "rhythm.json").read_text())
                self.assertIn("tempo_hypotheses", result)
                self.assertFalse(result["verified_bpm"])
                self.assertEqual(media.digest(source), before)
                self.assertEqual(media.verify("audio-test")["verified_artifacts"],
                                 report["verified_artifact_count"])
                with self.assertRaisesRegex(ValueError, "already exists"):
                    media.run(args)


if __name__ == "__main__":
    unittest.main()
