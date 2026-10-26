"""tools/transcribe_audio.py: Gemini errors are readable, models fall back, no key is reported."""
from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import transcribe_audio as ta  # noqa: E402


def http_error(code: int, body: dict) -> urllib.error.HTTPError:
    return urllib.error.HTTPError("https://x", code, "err", {}, io.BytesIO(json.dumps(body).encode()))


def ok_response(text: str):
    return io.BytesIO(json.dumps({"candidates": [{"content": {"parts": [{"text": text}]}}]}).encode())


BAD_KEY = {"error": {"code": 400, "message": "API key not valid. Please pass a valid API key.",
                     "status": "INVALID_ARGUMENT", "details": [{"reason": "API_KEY_INVALID"}]}}
NOT_FOUND = {"error": {"code": 404, "message": "models/x is not found", "status": "NOT_FOUND"}}


class TranscribeAudioTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.wav = Path(self.tmp.name) / "clip.wav"
        self.wav.write_bytes(b"RIFF" + b"\0" * 64)
        self.log: list[str] = []

    def tearDown(self):
        self.tmp.cleanup()

    def test_bad_key_message_is_shown_and_stops(self):
        calls = []

        def fake(req, timeout=0):
            calls.append(req.full_url)
            raise http_error(400, BAD_KEY)

        with mock.patch.object(ta.urllib.request, "urlopen", fake):
            with self.assertRaises(ta.GeminiError) as cm:
                ta.gemini_transcribe(self.wav, "p", ["m1", "m2"], "k", log=self.log.append)
        self.assertIn("API key not valid", str(cm.exception))
        self.assertIn("aistudio.google.com/apikey", str(cm.exception))
        self.assertEqual(len(calls), 1, "a bad key must not be retried on other models")

    def test_missing_model_falls_back_to_next(self):
        def fake(req, timeout=0):
            if "/m1:" in req.full_url:
                raise http_error(404, NOT_FOUND)
            return ok_response("مرحبا")

        with mock.patch.object(ta.urllib.request, "urlopen", fake):
            text, model = ta.gemini_transcribe(self.wav, "p", ["m1", "m2"], "k", log=self.log.append)
        self.assertEqual((text, model), ("مرحبا", "m2"))

    def test_rate_limit_is_retried(self):
        seq = [http_error(429, {"error": {"message": "quota", "status": "RESOURCE_EXHAUSTED"}})]

        def fake(req, timeout=0):
            if seq:
                raise seq.pop()
            return ok_response("تم")

        with mock.patch.object(ta.urllib.request, "urlopen", fake), mock.patch.object(ta.time, "sleep"):
            text, model = ta.gemini_transcribe(self.wav, "p", ["m1"], "k", log=self.log.append)
        self.assertEqual((text, model), ("تم", "m1"))

    def test_request_sends_key_header_and_inline_audio(self):
        seen = {}

        def fake(req, timeout=0):
            seen["key"] = req.get_header("X-goog-api-key")
            seen["body"] = json.loads(req.data)
            return ok_response("x")

        with mock.patch.object(ta.urllib.request, "urlopen", fake):
            ta.gemini_transcribe(self.wav, "p", ["m1"], "secret", log=self.log.append)
        self.assertEqual(seen["key"], "secret")
        part = seen["body"]["contents"][0]["parts"][0]["inlineData"]
        self.assertEqual(part["mimeType"], "audio/wav")

    def test_blocked_or_empty_answer_is_explained(self):
        with self.assertRaises(ta.GeminiError) as cm:
            ta.extract_text({"promptFeedback": {"blockReason": "SAFETY"}}, "m1")
        self.assertIn("SAFETY", str(cm.exception))

    def test_cli_without_key_reports_it(self):
        env = {k: v for k, v in ta.os.environ.items() if k not in ("GEMINI_API_KEY", "GOOGLE_API_KEY")}
        with mock.patch.dict(ta.os.environ, env, clear=True), \
                mock.patch("sys.stderr", new_callable=io.StringIO) as err:
            code = ta.main([str(self.wav), "--engine", "gemini"])
        self.assertEqual(code, 2)
        self.assertIn("GEMINI_API_KEY", err.getvalue())

    def test_cli_missing_file(self):
        with mock.patch("sys.stderr", new_callable=io.StringIO):
            self.assertEqual(ta.main([str(self.wav) + ".nope"]), 2)

    def test_413_on_last_attempt_still_switches_to_files_api(self):
        seq = [http_error(503, {"error": {"message": "busy"}}), http_error(413, {"error": {"message": "too big"}})]
        urls = []

        def fake(req, timeout=0):
            urls.append(req.full_url)
            if "upload/v1beta/files" in req.full_url and "upload_id" not in req.full_url:
                return mock.Mock(headers={"X-Goog-Upload-URL": "https://up/upload_id=1"})
            if "upload_id" in req.full_url:
                return io.BytesIO(json.dumps({"file": {"name": "files/a", "uri": "gs://a", "state": "ACTIVE"}}).encode())
            if seq:
                raise seq.pop(0)
            self.assertIn("fileData", req.data.decode())
            return ok_response("كبير")

        with mock.patch.object(ta.urllib.request, "urlopen", fake), mock.patch.object(ta.time, "sleep"):
            text, _ = ta.gemini_transcribe(self.wav, "p", ["m1"], "k", retries=1, log=self.log.append)
        self.assertEqual(text, "كبير")

    def test_files_api_poll_timeout_raises(self):
        def fake(req, timeout=0):
            if "upload_id" in req.full_url:
                return io.BytesIO(json.dumps({"file": {"name": "files/a", "uri": "gs://a", "state": "PROCESSING"}}).encode())
            if req.get_method() == "GET":
                return io.BytesIO(json.dumps({"name": "files/a", "uri": "gs://a", "state": "PROCESSING"}).encode())
            return mock.Mock(headers={"X-Goog-Upload-URL": "https://up/upload_id=1"})

        with mock.patch.object(ta.urllib.request, "urlopen", fake), mock.patch.object(ta.time, "sleep"):
            with self.assertRaises(ta.GeminiError) as cm:
                ta.upload_file(self.wav, "k", "audio/wav")
        self.assertIn("still PROCESSING", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
