"""Security regression checks for the optional reference media inspector."""
from __future__ import annotations

import importlib.util
import io
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parent.parent / ".claude/skills/kosif-superpowers/scripts/fetch_reference.py"
spec = importlib.util.spec_from_file_location("kosif_reference_fetch", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class ReferenceFetchSecurityTests(unittest.TestCase):
    def test_non_http_url_rejected(self):
        for url in ["file:///etc/passwd", "data:text/plain,hello", "ftp://example.org/a.ts"]:
            with self.subTest(url=url), self.assertRaises(mod.RefuseError):
                mod._validate_public_url(url)

    def test_local_ip_rejected(self):
        for ip in ("127.0.0.1", "10.0.0.2", "169.254.0.1"):
            with self.subTest(ip=ip), self.assertRaises(mod.RefuseError):
                mod._validate_public_url("http://" + ip + "/clip.ts")

    def test_playlist_key_match_not_substring(self):
        line = '#EXT-X-STREAM-INF:AVERAGE-BANDWIDTH=1000,BANDWIDTH=3000'
        self.assertEqual(mod.attr(line, "BANDWIDTH"), "3000")
        self.assertEqual(mod.attr(line, "AVERAGE-BANDWIDTH"), "1000")

    def test_hls_file_segment_rejected_at_request(self):
        parsed = mod.parse_media('#EXTM3U\nfile:///etc/passwd\n', 'https://example.org/master.m3u8')
        self.assertEqual(parsed["segments"], ["file:///etc/passwd"])
        with self.assertRaises(mod.RefuseError):
            mod._validate_public_url(parsed["segments"][0])

    def test_limited_response_bytes(self):
        class FakeResponse(io.BytesIO):
            headers = {"Content-Type": "text/plain"}
        with patch.object(mod, "_request", return_value=FakeResponse(b"x" * 20)):
            with self.assertRaises(mod.RefuseError):
                mod.fetch_bytes("https://example.org/oversized", retries=1, max_bytes=8)


if __name__ == "__main__":
    unittest.main()
