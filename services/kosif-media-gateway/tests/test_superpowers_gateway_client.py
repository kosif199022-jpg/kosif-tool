"""Offline security tests for the Superpowers gateway client; no vendor calls or credits."""
from __future__ import annotations

import http.server
import importlib.util
import os
import tempfile
import threading
import unittest
from pathlib import Path
from unittest import mock

_SCRIPT = Path(__file__).resolve().parents[3] / ".claude/skills/kosif-superpowers/scripts/_media_gateway.py"
_spec = importlib.util.spec_from_file_location("kosif_superpowers_gateway_client", _SCRIPT)
gateway = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gateway)


class _Target(http.server.BaseHTTPRequestHandler):
    hits = []

    def log_message(self, *_):
        pass

    def do_GET(self):
        type(self).hits.append(self.headers.get("Authorization"))
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"ok": true}')


class _Redirect(http.server.BaseHTTPRequestHandler):
    location = ""

    def log_message(self, *_):
        pass

    def do_GET(self):
        self.send_response(302)
        self.send_header("Location", self.location)
        self.end_headers()


class SuperpowersGatewayClientSecurityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.target = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _Target)
        cls.redirect = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _Redirect)
        _Redirect.location = f"http://127.0.0.1:{cls.target.server_port}/collect"
        cls.threads = [
            threading.Thread(target=s.serve_forever, daemon=True)
            for s in (cls.target, cls.redirect)
        ]
        for thread in cls.threads:
            thread.start()

    @classmethod
    def tearDownClass(cls):
        for server in (cls.redirect, cls.target):
            server.shutdown()
            server.server_close()
        for thread in cls.threads:
            thread.join(timeout=5)

    def setUp(self):
        _Target.hits.clear()
        self.env = mock.patch.dict(os.environ, {
            "KOSIF_GATEWAY_URL": f"http://127.0.0.1:{self.redirect.server_port}",
            "KOSIF_GATEWAY_TOKEN": "test-only-bearer-secret",
        })
        self.env.start()

    def tearDown(self):
        self.env.stop()

    def test_redirect_is_not_followed_or_authorized_again(self):
        status, body = gateway._call("GET", "/v1/providers/snapany/status", timeout=5)
        self.assertEqual(status, 302)
        self.assertEqual(body["error"], "GATEWAY_REDIRECT_BLOCKED")
        self.assertEqual(_Target.hits, [])

    def test_file_download_redirect_is_blocked_without_partial_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "clip.mp4"
            with self.assertRaises(gateway.GatewayError):
                gateway._fetch("/v1/files/testticket", output, "0" * 64, 100)
            self.assertFalse(output.exists())
            self.assertFalse(output.with_name("clip.mp4.part").exists())
            self.assertEqual(_Target.hits, [])

    def test_path_and_name_traversal_are_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            for filename in ("../outside.mp4", "folder/clip.mp4", r"folder\clip.mp4", "..", ""):
                with self.assertRaises(gateway.GatewayError):
                    gateway._destination(out, filename)
            for file_path in ("/v1/files/../secret", "//other.host/file", "/v1/files/id?token=secret", "/v1/files/"):
                with self.assertRaises(gateway.GatewayError):
                    gateway._fetch(file_path, out / "safe.mp4", "0" * 64, 5)

    def test_origin_validation(self):
        for url in ("ftp://localhost", "http://example.org", "https://user:pw@example.org",
                    "https://example.org/path", "https://example.org/?secret=1"):
            with mock.patch.dict(os.environ, {"KOSIF_GATEWAY_URL": url}):
                with self.assertRaises(gateway.GatewayError):
                    gateway.config()

    def test_snapany_status_is_nonbillable_get(self):
        with mock.patch.object(gateway, "_call", return_value=(200, {"ok": True, "configured": True})) as called:
            self.assertTrue(gateway.snapany_status()["configured"])
        called.assert_called_once_with("GET", "/v1/providers/snapany/status", timeout=30)


if __name__ == "__main__":
    unittest.main()
