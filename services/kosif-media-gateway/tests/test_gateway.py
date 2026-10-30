"""Offline tests for the KOSIF Media Gateway (stub yt-dlp, real ffmpeg, real HTTP, real MCP client).

Run: python3 -m unittest discover -s services/kosif-media-gateway/tests -v
"""
from __future__ import annotations

import asyncio
import hashlib
import importlib.util
import json
import os
import shutil
import sys
import tempfile
import threading
import time
import unittest
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOKEN = "test-token-" + "x" * 32
os.environ["KOSIF_GATEWAY_TOKEN"] = TOKEN
os.environ.setdefault("KOSIF_DOWNLOADS_PER_HOUR", "50")
os.environ["KOSIF_BLOCK_COOLDOWN"] = "120"
if not os.environ.get("KOSIF_FFMPEG"):
    ff = shutil.which("ffmpeg")
    if not ff:
        import imageio_ffmpeg  # noqa: PLC0415
        ff = imageio_ffmpeg.get_ffmpeg_exe()
    os.environ["KOSIF_FFMPEG"] = ff

spec = importlib.util.spec_from_file_location("gateway_server", HERE.parent / "server.py")
gw = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gw)
gw.YTDLP_CMD = [sys.executable, str(HERE / "stub_ytdlp.py")]


def reset(mode: str = "ok") -> None:
    os.environ["STUB_MODE"] = mode
    with gw._LOCK:
        gw._STATE["blocked_until"] = 0.0
        gw._STATE["last_youtube"] = None
        gw._STATE["verified_downloads"] = 0
        gw._ATTEMPTS.clear()
        for job in gw._JOBS.values():
            shutil.rmtree(job["folder"], ignore_errors=True)
        gw._JOBS.clear()


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.srv = gw.make_server(0, "127.0.0.1")
        cls.port = cls.srv.server_address[1]
        cls.base = f"http://127.0.0.1:{cls.port}"
        threading.Thread(target=cls.srv.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()
        cls.srv.server_close()

    def setUp(self):
        reset()

    def req(self, method, path, body=None, token=TOKEN, raw=None, headers=None):
        data = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)
        h = {"Content-Type": "application/json", **(headers or {})}
        if token:
            h["Authorization"] = "Bearer " + token
        r = urllib.request.Request(self.base + path, data=data, method=method, headers=h)
        try:
            with urllib.request.urlopen(r, timeout=120) as resp:
                return resp.status, dict(resp.headers), resp.read()
        except urllib.error.HTTPError as e:
            return e.code, dict(e.headers), e.read()

    def jreq(self, *a, **k):
        code, headers, body = self.req(*a, **k)
        return code, headers, (json.loads(body) if body else None)


class TestSources(unittest.TestCase):
    def test_ids_and_urls(self):
        ok = {"dYrEeavC3cw": "dYrEeavC3cw",
              "https://www.youtube.com/watch?v=dYrEeavC3cw&t=3": "dYrEeavC3cw",
              "https://youtu.be/dYrEeavC3cw": "dYrEeavC3cw",
              "https://youtube.com/shorts/dYrEeavC3cw": "dYrEeavC3cw",
              "https://m.youtube.com/watch?v=dYrEeavC3cw": "dYrEeavC3cw"}
        for s, want in ok.items():
            self.assertEqual(gw.video_id(s), want, s)
        for bad in ["", "short", "dYrEeavC3cw0", "dYrEeavC3c!", "https://evil.com/watch?v=dYrEeavC3cw",
                    "https://user:pw@youtube.com/watch?v=dYrEeavC3cw", "https://youtube.com:8443/watch?v=dYrEeavC3cw",
                    "-dYrEeavC3c --exec", "file:///etc/passwd"]:
            self.assertIsNone(gw.video_id(bad), bad)

    def test_ssrf_guard(self):
        self.assertIsNone(gw.parse_source("https://169.254.169.254/latest"))
        self.assertIsNone(gw.parse_source("http://upload.wikimedia.org/x.webm"))
        self.assertEqual(gw.parse_source("https://upload.wikimedia.org/a/b.webm")["kind"], "url")

    def test_classify(self):
        self.assertEqual(gw.classify("ERROR: Sign in to confirm you're not a bot")["code"], "YOUTUBE_LOGIN_REQUIRED")
        self.assertEqual(gw.classify("ERROR: HTTP Error 429: Too Many Requests")["code"], "YOUTUBE_HTTP_429")
        self.assertEqual(gw.classify("ERROR: Tunnel connection failed: 502 Bad Gateway")["code"], "YOUTUBE_PROXY_502")
        self.assertEqual(gw.classify("ERROR: HTTP Error 403: Forbidden")["code"], "YOUTUBE_HTTP_403")
        self.assertEqual(gw.classify("ERROR: This video is DRM protected")["code"], "DRM_PROTECTED")
        d = gw.classify("ERROR: fail https://secret.example/token=abc")
        self.assertNotIn("secret.example", d["detail"])


class TestHttp(Base):
    def test_health_is_public_and_runs_deps(self):
        code, _, body = self.jreq("GET", "/health", token=None)
        self.assertEqual(code, 200)
        self.assertTrue(body["alive"])
        self.assertTrue(body["dependencies"]["yt_dlp"])
        self.assertTrue(body["dependencies"]["ffmpeg"])
        self.assertFalse(body["youtube_download_verified"])

    def test_browser_page_is_public(self):
        code, headers, body = self.req("GET", "/browser", token=None)
        self.assertEqual(code, 200)
        self.assertIn("text/html", headers["Content-Type"])
        self.assertIn(b"KOSIF Video Browser", body)

    def test_auth_failures(self):
        for tok in (None, "wrong", TOKEN + "x", TOKEN[:-1]):
            code, headers, body = self.jreq("POST", "/v1/probe", {"video": "dYrEeavC3cw"}, token=tok)
            self.assertEqual(code, 401, tok)
            self.assertIn("Bearer", headers.get("WWW-Authenticate", ""))
        code, _, _ = self.jreq("GET", "/v1/files/abc", token=None)
        self.assertEqual(code, 401)

    def test_keepalive_after_401_with_body(self):
        """Claude Code reuses the connection: a rejected POST must not leave its body behind."""
        import http.client  # noqa: PLC0415
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=30)
        body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "ping"})
        conn.request("POST", "/mcp", body, {"Authorization": "Bearer wrong", "Content-Type": "application/json"})
        r = conn.getresponse()
        r.read()
        self.assertEqual(r.status, 401)
        conn.request("POST", "/mcp", body, {"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"})
        r = conn.getresponse()
        self.assertEqual((r.status, json.loads(r.read())["result"]), (200, {}))
        conn.close()

    def test_bad_requests(self):
        self.assertEqual(self.jreq("POST", "/v1/probe", raw=b"{not json")[0], 400)
        self.assertEqual(self.jreq("POST", "/v1/probe", raw=b"x" * 9000)[0], 413)
        self.assertEqual(self.jreq("POST", "/v1/probe", ["list"])[0], 400)
        code, _, body = self.jreq("POST", "/v1/probe", {"video": "not-an-id"})
        self.assertEqual((code, body["error"]), (400, "INVALID_SOURCE"))
        code, _, body = self.jreq("POST", "/v1/download", {"video": "dYrEeavC3cw"})
        self.assertEqual((code, body["error"]), (400, "EXPLICIT_DOWNLOAD_PERMISSION_REQUIRED"))
        code, _, body = self.jreq("POST", "/v1/download", {"video": "dYrEeavC3cw", "rights": "owned", "quality": 4320})
        self.assertEqual(body["error"], "INVALID_QUALITY")
        self.assertEqual(self.jreq("POST", "/v1/nope", {})[0], 404)

    def test_probe_ok(self):
        code, _, body = self.jreq("POST", "/v1/probe", {"video": "https://youtube.com/shorts/dYrEeavC3cw"})
        self.assertEqual(code, 200)
        self.assertEqual(body["h264_formats"], 1)
        self.assertFalse(body["downloaded"])

    def test_probe_media_check(self):
        code, _, body = self.jreq("POST", "/v1/probe", {"video": "dYrEeavC3cw", "media_check": True})
        self.assertEqual((code, body["media_access"]["code"], body["media_access"]["bytes_read"]), (200, "OK", 10240))
        reset("probe_only_403")   # metadata readable, media stream refused: the real cloud pattern
        code, _, body = self.jreq("POST", "/v1/probe", {"video": "dYrEeavC3cw", "media_check": True})
        self.assertEqual((code, body["error"]), (422, "YOUTUBE_HTTP_403"))
        self.assertEqual(body["title"], "stub")
        self.assertEqual(self.jreq("POST", "/v1/probe", {"video": "dYrEeavC3cw"})[0], 429, "cool-down after a block")

    def test_block_sets_cooldown_and_stops_retries(self):
        counter = Path(tempfile.mkdtemp()) / "calls"
        os.environ["STUB_COUNTER"] = str(counter)
        try:
            for mode, code in (("login", "YOUTUBE_LOGIN_REQUIRED"), ("429", "YOUTUBE_HTTP_429"),
                               ("proxy502", "YOUTUBE_PROXY_502"), ("403", "YOUTUBE_HTTP_403")):
                reset(mode)
                counter.write_text("")
                status_code, _, body = self.jreq("POST", "/v1/probe", {"video": "dYrEeavC3cw"})
                self.assertEqual((status_code, body["error"], body["retried"]), (422, code, False))
                s2, headers, b2 = self.jreq("POST", "/v1/download", {"video": "dYrEeavC3cw", "rights": "owned"})
                self.assertEqual(s2, 429)
                self.assertGreater(b2["cooldown_seconds"], 0)
                self.assertEqual(counter.read_text().count("call"), 1, "no second request during cool-down")
        finally:
            os.environ.pop("STUB_COUNTER", None)

    def _download(self, mode="ok", quality=720):
        reset(mode)
        return self.jreq("POST", "/v1/download", {"video": "dYrEeavC3cw", "rights": "owned", "quality": quality})

    def test_download_verified_original_and_lossless_remux(self):
        code, _, body = self._download()
        self.assertEqual(code, 200, body)
        self.assertTrue(body["verified"])
        roles = {f["role"]: f for f in body["files"]}
        self.assertEqual(set(roles), {"original", "compatible"})
        self.assertTrue(roles["compatible"]["lossless"])
        self.assertEqual(roles["compatible"]["method"], "remux")
        orig = roles["original"]
        self.assertEqual((orig["media"]["width"], orig["media"]["height"]), (360, 640))
        self.assertEqual(orig["media"]["orientation"], "portrait")
        self.assertAlmostEqual(orig["media"]["duration"], 3, delta=0.2)
        for f in body["files"]:
            c, headers, data = self.req("GET", f["file_path"])
            self.assertEqual(c, 200)
            self.assertEqual(hashlib.sha256(data).hexdigest(), f["sha256"])
            self.assertEqual(len(data), f["size_bytes"])
            self.assertEqual(headers["X-Content-SHA256"], f["sha256"])
        self.assertTrue(self.jreq("GET", "/health")[2]["youtube_download_verified"])

    def test_non_h264_is_transcoded_and_original_kept(self):
        if not gw.dependencies()["libx264"]:
            self.skipTest("ffmpeg without libx264")
        code, _, body = self._download("mpeg4")
        self.assertEqual(code, 200, body)
        roles = {f["role"]: f for f in body["files"]}
        self.assertEqual(roles["original"]["media"]["vcodec"], "mpeg4")
        self.assertEqual(roles["compatible"]["media"]["vcodec"], "h264")
        self.assertFalse(roles["compatible"]["lossless"])

    def test_corrupt_and_incomplete_rejected_and_cleaned(self):
        before = set(Path(tempfile.gettempdir()).glob(gw.TEMP_PREFIX + "*"))
        for mode in ("corrupt", "short"):
            code, _, body = self._download(mode)
            self.assertEqual(code, 422, body)
            self.assertFalse(body["ok"])
            self.assertIn(body["error"], ("NO_VIDEO_STREAM", "CORRUPT_OR_INCOMPLETE", "INCOMPLETE_DURATION"))
            self.assertNotIn("files", body)
        self.assertEqual(set(Path(tempfile.gettempdir()).glob(gw.TEMP_PREFIX + "*")), before, "temp folders removed")

    def test_too_large(self):
        code, _, body = self._download("big")
        self.assertEqual(body["error"], "FILE_TOO_LARGE")

    def test_timeout(self):
        old = gw.DOWNLOAD_TIMEOUT
        gw.DOWNLOAD_TIMEOUT = 2
        os.environ["STUB_SLEEP"] = "6"
        try:
            code, _, body = self._download("slow")
            self.assertEqual((code, body["error"]), (504, "DOWNLOAD_TIMEOUT"))
        finally:
            gw.DOWNLOAD_TIMEOUT = old

    def test_concurrency_one_at_a_time(self):
        reset("slow")
        os.environ["STUB_SLEEP"] = "3"
        results = []
        t = threading.Thread(target=lambda: results.append(
            self.jreq("POST", "/v1/download", {"video": "dYrEeavC3cw", "rights": "owned"})))
        t.start()
        time.sleep(0.8)
        code, headers, body = self.jreq("POST", "/v1/download", {"video": "dYrEeavC3cw", "rights": "owned"})
        t.join()
        self.assertEqual((code, body["error"]), (409, "BUSY_ONE_DOWNLOAD_AT_A_TIME"))
        self.assertIn("Retry-After", headers)
        self.assertEqual(results[0][0], 200)

    def test_rate_limit(self):
        old = gw.PER_HOUR
        gw.PER_HOUR = 1
        try:
            self.assertEqual(self._download()[0], 200)
            code, headers, body = self.jreq("POST", "/v1/download", {"video": "dYrEeavC3cw", "rights": "owned"})
            self.assertEqual((code, body["error"]), (429, "RATE_LIMIT_PER_HOUR"))
        finally:
            gw.PER_HOUR = old

    def test_files_expire_and_are_deleted(self):
        code, _, body = self._download()
        folder = next(iter(gw._JOBS.values()))["folder"]
        for job in gw._JOBS.values():
            job["expires"] = 0
        gw.prune()
        self.assertFalse(Path(folder).exists())
        self.assertEqual(self.jreq("GET", body["files"][0]["file_path"])[0], 404)


class TestUpload(Base):
    """Files the owner's iPhone (a-Shell) downloaded and sends in: POST /v1/upload, GET /v1/inbox, MCP list_uploads."""

    def make_mp4(self, codec=("-c:v", "libx264", "-pix_fmt", "yuv420p")):
        out = Path(tempfile.mkdtemp()) / "clip.mp4"
        import subprocess  # noqa: PLC0415
        subprocess.run([os.environ["KOSIF_FFMPEG"], "-y", "-v", "error", "-f", "lavfi", "-i", "testsrc2=s=360x640:r=25:d=2",
                        "-f", "lavfi", "-i", "sine=d=2", *codec, "-c:a", "aac", "-shortest", str(out)], check=True)
        return out

    def up(self, data, token=TOKEN, name="Clip One.mp4"):
        return self.jreq("POST", "/v1/upload", raw=data, token=token,
                         headers={"Content-Type": "video/mp4", "X-Filename": name,
                                  "X-Source-Url": "https://youtube.com/shorts/dYrEeavC3cw"})

    def test_upload_verify_inbox_and_fetch(self):
        data = self.make_mp4().read_bytes()
        code, _, body = self.up(data)
        self.assertEqual(code, 200, body)
        roles = {f["role"]: f for f in body["files"]}
        self.assertEqual(roles["original"]["sha256"], hashlib.sha256(data).hexdigest())
        self.assertEqual(roles["original"]["media"]["orientation"], "portrait")
        self.assertTrue(roles["compatible"]["lossless"])
        code, _, box = self.jreq("GET", "/v1/inbox")
        self.assertEqual(box["uploads"][0]["upload_id"], body["upload_id"])
        self.assertEqual(box["uploads"][0]["name"], "Clip_One")
        c, _, got = self.req("GET", roles["original"]["file_path"])
        self.assertEqual(got, data)
        mcp = self.jreq("POST", "/mcp", {"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                                         "params": {"name": "list_uploads", "arguments": {}}})[2]
        self.assertEqual(mcp["result"]["structuredContent"]["uploads"][0]["upload_id"], body["upload_id"])

    def test_upload_rejects_bad_auth_corrupt_and_truncated(self):
        data = self.make_mp4().read_bytes()
        self.assertEqual(self.up(data, token="wrong")[0], 401)
        code, _, body = self.up(data[: len(data) // 2])
        self.assertEqual(code, 422)
        self.assertFalse(body["ok"])
        self.assertEqual(self.jreq("GET", "/v1/inbox")[2]["uploads"], [])
        import http.client  # noqa: PLC0415  (declared length larger than what arrives)
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=10)
        conn.putrequest("POST", "/v1/upload")
        conn.putheader("Authorization", "Bearer " + TOKEN)
        conn.putheader("Content-Length", str(len(data) + 5000))
        conn.endheaders()
        conn.send(data)
        conn.sock.shutdown(1)
        r = conn.getresponse()
        self.assertEqual(json.loads(r.read())["error"], "UPLOAD_INCOMPLETE")
        conn.close()

    def test_upload_size_limit(self):
        old = gw.UPLOAD_MB
        gw.UPLOAD_MB = 1
        try:
            import http.client  # noqa: PLC0415  (curl's Expect: 100-continue: refused before any byte is sent)
            for tok, want in ((TOKEN, 413), ("wrong", 401)):
                conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=10)
                conn.putrequest("POST", "/v1/upload")
                conn.putheader("Authorization", "Bearer " + tok)
                conn.putheader("Content-Length", str(1024 * 1024 + 10))
                conn.putheader("Expect", "100-continue")
                conn.endheaders()
                r = conn.getresponse()
                self.assertEqual(r.status, want)
                conn.close()
        finally:
            gw.UPLOAD_MB = old

    def test_send_script_is_served(self):
        code, headers, body = self.req("GET", "/kosif-send.sh", token=None)
        self.assertEqual(code, 200)
        self.assertTrue(body.startswith(b"#!/bin/sh"))
        self.assertNotIn(TOKEN.encode(), body)


class TestSuperpowersClient(Base):
    """The KOSIF Superpowers client (_media_gateway.py, used by fetch_video.py --gateway) end to end."""

    def setUp(self):
        super().setUp()
        skill = HERE.parents[2] / ".claude" / "skills" / "kosif-superpowers" / "scripts"
        sys.path.insert(0, str(skill))
        import _media_gateway  # noqa: PLC0415
        self.client = _media_gateway
        os.environ["KOSIF_GATEWAY_URL"] = self.base
        self.out = Path(tempfile.mkdtemp())

    def tearDown(self):
        os.environ.pop("KOSIF_GATEWAY_URL", None)
        shutil.rmtree(self.out, ignore_errors=True)

    def test_download_verifies_hash_and_keeps_original(self):
        rec = self.client.download("https://youtu.be/dYrEeavC3cw", self.out, "owned", 720)
        self.assertTrue(rec["verified"], rec)
        self.assertTrue(Path(rec["original_file"]).is_file())
        self.assertTrue(Path(rec["safe_file"]).is_file())
        self.assertEqual(hashlib.sha256(Path(rec["original_file"]).read_bytes()).hexdigest(), rec["sha256"])
        self.assertEqual((rec["width"], rec["height"]), (360, 640))
        self.assertFalse(list(self.out.glob("*.part")))

    def test_pull_latest_upload(self):
        clip = TestUpload.make_mp4(self)
        code, _, body = self.jreq("POST", "/v1/upload", raw=clip.read_bytes(), headers={"X-Filename": "a.mp4"})
        self.assertEqual(code, 200, body)
        rec = self.client.pull("", self.out)
        self.assertEqual(rec["upload_id"], body["upload_id"])
        self.assertEqual(Path(rec["original_file"]).read_bytes(), clip.read_bytes())
        self.assertFalse(self.client.pull("nope", self.out)["ok"])

    def test_blocked_is_reported(self):
        reset("login")
        rec = self.client.download("dYrEeavC3cw", self.out, "owned")
        self.assertIsNone(rec["file"])
        self.assertTrue(rec["blocked"])
        self.assertEqual(rec["error"], "YOUTUBE_LOGIN_REQUIRED")
        self.assertFalse(list(self.out.iterdir()))

    def test_client_without_token_refuses(self):
        old = os.environ.pop("KOSIF_GATEWAY_TOKEN")
        try:
            self.assertFalse(self.client.available())
            with self.assertRaises(self.client.GatewayError):
                self.client.probe("dYrEeavC3cw")
        finally:
            os.environ["KOSIF_GATEWAY_TOKEN"] = old


class TestMcpRaw(Base):
    def rpc(self, payload, token=TOKEN):
        return self.jreq("POST", "/mcp", payload, token=token,
                         headers={"Accept": "application/json, text/event-stream"})

    def test_lifecycle(self):
        code, _, body = self.rpc({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                                  "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                                             "clientInfo": {"name": "t", "version": "1"}}})
        self.assertEqual(body["result"]["protocolVersion"], "2025-06-18")
        self.assertEqual(self.rpc({"jsonrpc": "2.0", "method": "notifications/initialized"})[0], 202)
        self.assertEqual(self.rpc({"jsonrpc": "2.0", "method": "notifications/cancelled",
                                   "params": {"requestId": 1}})[0], 202)
        names = [t["name"] for t in self.rpc({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})[2]["result"]["tools"]]
        self.assertEqual(names, ["gateway_status", "list_uploads", "probe_youtube", "download_permitted_video"])
        unknown = self.rpc({"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "nope"}})[2]
        self.assertEqual(unknown["error"]["code"], -32602)
        self.assertEqual(self.rpc({"jsonrpc": "2.0", "id": 4, "method": "x/y"})[2]["error"]["code"], -32601)
        self.assertEqual(self.rpc({"id": 5, "method": "ping"})[2]["error"]["code"], -32600)
        batch = self.rpc([{"jsonrpc": "2.0", "id": 6, "method": "ping"}, {"jsonrpc": "2.0", "method": "notifications/x"}])[2]
        self.assertEqual(batch, [{"jsonrpc": "2.0", "id": 6, "result": {}}])
        self.assertEqual(self.rpc({"jsonrpc": "2.0", "id": 7, "method": "ping"}, token="bad")[0], 401)
        self.assertEqual(self.jreq("GET", "/mcp")[0], 405)
        self.assertEqual(self.jreq("POST", "/mcp", raw=b"{bad")[2]["error"]["code"], -32700)

    def test_tool_error_is_reported_not_raised(self):
        reset("login")
        body = self.rpc({"jsonrpc": "2.0", "id": 9, "method": "tools/call",
                         "params": {"name": "probe_youtube", "arguments": {"video": "dYrEeavC3cw"}}})[2]
        self.assertTrue(body["result"]["isError"])
        self.assertEqual(body["result"]["structuredContent"]["error"], "YOUTUBE_LOGIN_REQUIRED")


class TestMcpSdkClient(Base):
    """The official MCP Python SDK as the client: initialize, tools/list, tools/call over Streamable HTTP."""

    def test_sdk_client(self):
        try:
            from mcp_client_check import run_check  # noqa: PLC0415
        except ImportError as exc:
            self.skipTest(f"mcp SDK not installed: {exc}")
        report = asyncio.run(run_check(self.base + "/mcp", TOKEN, download=True))
        self.assertTrue(report["initialize"]["ok"], report)
        self.assertIn("download_permitted_video", report["tools"])
        self.assertTrue(report["calls"]["gateway_status"]["ok"])
        self.assertTrue(report["calls"]["download_permitted_video"]["ok"], report)
        bad = asyncio.run(run_check(self.base + "/mcp", "wrong-token", download=False))
        self.assertFalse(bad["initialize"]["ok"])


sys.path.insert(0, str(HERE.parent))

if __name__ == "__main__":
    unittest.main()
