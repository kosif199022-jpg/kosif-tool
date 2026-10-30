"""Offline contract tests for the opt-in SnapAny API adapter; never bill the actual provider."""
from __future__ import annotations
import importlib.util
import io
import json
import os
from pathlib import Path
import unittest
from unittest import mock

_SRC = Path(__file__).resolve().parents[1] / "snapany_provider.py"
_spec = importlib.util.spec_from_file_location("snapany_provider_for_tests", _SRC)
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)

_VIDEO = "https://www.youtube.com/watch?v=dYrEeavC3cw"
_FIXTURE = {
    "title": "Public test video",
    "medias": [{
        "media_type": "video",
        "variants": [
            {"quality": 1080, "video_proxy_url": "https://proxy.example.net/video?token=mock", "audio_proxy_url": "https://proxy.example.net/audio?token=mock"},
            {"quality": 2160, "video_proxy_url": "https://proxy.example.net/4k"},
            {"quality": 720, "video_proxy_url": "https://proxy.example.net/720"},
            {"quality": 360, "video_proxy_url": "http://insecure.example.net/video"}
        ]
    }]
}


class _Response:
    def __init__(self, body):
        self.body = io.BytesIO(json.dumps(body).encode())
    def __enter__(self):
        return self
    def __exit__(self, *_):
        return False
    def read(self, n):
        return self.body.read(n)


class SnapAnyProviderTest(unittest.TestCase):
    def setUp(self):
        mod._TIMES.clear()
        env = {
            "KOSIF_SNAPANY_API_KEY": "",
            "KOSIF_SNAPANY_ENABLED": "0",
        }
        self.patch = mock.patch.dict(os.environ, env)
        self.patch.start()

    def tearDown(self):
        self.patch.stop()
        mod._TIMES.clear()

    def test_disabled_by_default_and_never_calls_vendor(self):
        with mock.patch.object(mod.urllib.request, "urlopen", side_effect=AssertionError("should not call")):
            out = mod.resolve(_VIDEO, "cc-licensed", 720, True)
        self.assertFalse(out["ok"])
        self.assertEqual(out["error"], "SNAPANY_NOT_CONFIGURED")

    def test_explicit_consent_required(self):
        os.environ["KOSIF_SNAPANY_ENABLED"] = "1"
        os.environ["KOSIF_SNAPANY_API_KEY"] = "mock-secret"
        with mock.patch.object(mod.urllib.request, "urlopen", side_effect=AssertionError("should not call")):
            out = mod.resolve(_VIDEO, "owned", 720, False)
        self.assertEqual(out["error"], "CREDIT_SPEND_CONFIRMATION_REQUIRED")

    def test_rights_and_url_required(self):
        self.assertEqual(mod.resolve("https://unknown.example/", "owned", 720, True)["error"], "INVALID_YOUTUBE_URL")
        self.assertEqual(mod.resolve(_VIDEO, "unknown", 720, True)["error"], "DOWNLOAD_RIGHTS_REQUIRED")
        self.assertEqual(mod.resolve(_VIDEO, "owned", 2160, True)["error"], "INVALID_QUALITY")

    def test_official_endpoint_and_only_proxy_links_exposed(self):
        os.environ["KOSIF_SNAPANY_ENABLED"] = "1"
        os.environ["KOSIF_SNAPANY_API_KEY"] = "mock-secret"
        seen = []
        def fake_open(req, timeout):
            seen.append(req)
            self.assertEqual(req.full_url, "https://api.snapany.com/openapi/v1/youtube/proxy-download")
            self.assertEqual(json.loads(req.data)["url"], _VIDEO)
            return _Response(_FIXTURE)
        with mock.patch.object(mod.urllib.request, "urlopen", fake_open):
            out = mod.resolve(_VIDEO, "public-domain", 1080, True)
        self.assertTrue(out["ok"])
        self.assertFalse(out["downloaded"])
        self.assertTrue(out["credits_may_have_been_charged"])
        self.assertEqual([o["quality"] for o in out["options"]], [1080, 720])
        self.assertTrue(out["options"][0]["requires_mux"])
        self.assertEqual(len(seen), 1)

    def test_daily_cap(self):
        os.environ["KOSIF_SNAPANY_ENABLED"] = "1"
        os.environ["KOSIF_SNAPANY_API_KEY"] = "mock-secret"
        with mock.patch.object(mod.urllib.request, "urlopen", return_value=_Response(_FIXTURE)) as called:
            for _ in range(2):
                self.assertTrue(mod.resolve(_VIDEO, "owned", 720, True)["ok"])
            third = mod.resolve(_VIDEO, "owned", 720, True)
        self.assertEqual(third["error"], "PROVIDER_DAILY_LIMIT")
        self.assertEqual(called.call_count, 2)

    def test_no_keys_in_status(self):
        os.environ["KOSIF_SNAPANY_ENABLED"] = "1"
        os.environ["KOSIF_SNAPANY_API_KEY"] = "never-expose-this-secret"
        status = json.dumps(mod.status())
        self.assertNotIn("never-expose-this-secret", status)
        self.assertTrue(mod.status()["configured"])


if __name__ == "__main__":
    unittest.main()
