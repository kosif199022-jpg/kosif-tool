"""Offline tests for the kosif-voice-studio skill: a fake VoiceStudio backend stands in for the real one."""
import importlib.util
import io
import json
import math
import shutil
import struct
import tempfile
import threading
import unittest
import wave
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".claude/skills/kosif-voice-studio/scripts/voice_studio.py"
spec = importlib.util.spec_from_file_location("voice_studio", SCRIPT)
vsm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vsm)
HAS_FF = bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))


def tone_wav(seconds=0.6, amp=0.3) -> bytes:
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(16000)
        w.writeframes(b"".join(struct.pack("<h", int(amp * 32767 * math.sin(2 * math.pi * 440 * i / 16000)))
                               for i in range(int(16000 * seconds))))
    return buf.getvalue()


class Fake(BaseHTTPRequestHandler):
    seen: list = []
    token = None

    def log_message(self, *a):
        pass

    def _send(self, code, body, ctype="application/json"):
        data = body if isinstance(body, bytes) else json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _auth(self):
        if Fake.token and self.headers.get("Authorization") != f"Bearer {Fake.token}":
            self._send(401, {"detail": "auth"})
            return False
        return True

    def do_GET(self):
        if not self._auth():
            return
        if self.path == "/health":
            return self._send(200, {"status": "ok", "device": "cpu"})
        if self.path == "/openapi.json":  # routes live under a prefix, as versions may change
            return self._send(200, {"paths": {"/api/profiles": {"post": {}, "get": {}},
                                              "/api/design/describe": {"post": {}},
                                              "/v1/audio/speech": {"post": {}}}})
        if self.path == "/v1/audio/voices":
            return self._send(200, {"voices": [{"id": "p1", "name": "King"}]})
        self._send(404, {"detail": "nope"})

    def do_POST(self):
        if not self._auth():
            return
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        Fake.seen.append((self.path, self.headers.get("Content-Type", ""), body))
        if self.path == "/v1/audio/speech":
            return self._send(200, tone_wav(), "audio/wav")
        if self.path == "/v1/audio/transcriptions":
            return self._send(200, {"text": "صباح الفل", "language": "ar",
                                    "segments": [{"start": 0, "end": 1.2, "text": "صباح الفل"}],
                                    "words": [{"word": "صباح", "start": 0.0, "end": 0.6},
                                              {"word": "الفل", "start": 0.5, "end": 1.2}]})
        if self.path == "/api/design/describe":
            desc = json.loads(body)["description"]
            if "robot" in desc:
                return self._send(200, {"attrs": {}, "instruct": "", "matched": [], "unmatched": ["robot"]})
            return self._send(200, {"attrs": {"Gender": "male", "Age": "elderly"}, "instruct": "male, elderly",
                                    "matched": [{"category": "Gender", "token": "male"}], "unmatched": []})
        if self.path == "/api/profiles":
            return self._send(200, {"id": "prof_1"})
        self._send(404, {"detail": "nope"})


class WithServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.srv = ThreadingHTTPServer(("127.0.0.1", 0), Fake)
        threading.Thread(target=cls.srv.serve_forever, daemon=True).start()
        cls.url = f"http://127.0.0.1:{cls.srv.server_address[1]}"

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()

    def setUp(self):
        Fake.seen.clear()
        Fake.token = None
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_cli(self, *args):
        return vsm.main(["--url", self.url, "--json", *args])


class TestPure(unittest.TestCase):
    def test_self_test(self):
        self.assertEqual(vsm.self_test(), 0)

    def test_edge_word_ticks_become_seconds_and_never_overlap(self):
        w = vsm.edge_words([{"type": "WordBoundary", "offset": 10_000_000, "duration": 9_000_000, "text": "أ"},
                            {"type": "WordBoundary", "offset": 15_000_000, "duration": 1_000_000, "text": "ب"}])
        self.assertEqual(w, [{"word": "أ", "start": 1.0, "end": 1.5}, {"word": "ب", "start": 1.5, "end": 1.6}])

    def test_subtitles(self):
        segs = [{"start": 0.0, "end": 1.5, "text": "سلام"}, {"start": 61.0, "end": 62.0, "text": "تاني"}]
        srt = vsm.to_subtitles(segs, "srt")
        self.assertIn("2\n00:01:01,000 --> 00:01:02,000\nتاني", srt)
        self.assertIn("00:00:00.000 --> 00:00:01.500", vsm.to_subtitles(segs, "vtt"))

    def test_ca_bundle_is_honoured_only_when_it_exists(self):
        import os
        old = os.environ.pop("SSL_CERT_FILE", None), os.environ.pop("REQUESTS_CA_BUNDLE", None)
        try:
            os.environ["SSL_CERT_FILE"] = "/no/such/file.pem"
            self.assertIsNone(vsm.ca_context())
        finally:
            os.environ.pop("SSL_CERT_FILE", None)
            if old[0]:
                os.environ["SSL_CERT_FILE"] = old[0]
            if old[1]:
                os.environ["REQUESTS_CA_BUNDLE"] = old[1]


@unittest.skipUnless(HAS_FF, "ffmpeg/ffprobe not installed")
class TestVerify(unittest.TestCase):
    def test_error_body_is_not_audio(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "speech.wav"
            p.write_text('{"detail": "model not installed"}')
            with self.assertRaises(vsm.Fail) as cm:
                vsm.verify_audio(p)
            self.assertIn("not audio", str(cm.exception))

    def test_silence_is_flagged(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "s.wav"
            p.write_bytes(tone_wav(amp=0.0))
            rep = vsm.verify_audio(p)
            self.assertFalse(rep["ok"])
            p.write_bytes(tone_wav())
            self.assertTrue(vsm.verify_audio(p)["ok"])


class TestVoiceStudioApi(WithServer):
    def test_route_discovery_follows_openapi_prefix(self):
        vs = vsm.VoiceStudio(self.url)
        self.assertEqual(vs.path("/profiles"), "/api/profiles")
        with self.assertRaises(vsm.Fail):
            vs.path("/dub")

    def test_down_backend_is_reported_not_hidden(self):
        vs = vsm.VoiceStudio("http://127.0.0.1:9")
        self.assertFalse(vs.up())
        self.assertFalse(vsm.doctor(vs)["engines"]["voicestudio"]["ready"])

    def test_auth_failure_names_the_token(self):
        Fake.token = "s3cret"
        with self.assertRaises(vsm.Fail) as cm:
            vsm.VoiceStudio(self.url, token="").voices()
        self.assertIn("VOICESTUDIO_TOKEN", str(cm.exception))
        self.assertNotIn("s3cret", str(cm.exception))
        self.assertEqual(vsm.VoiceStudio(self.url, token="s3cret").voices()["voices"][0]["id"], "p1")

    @unittest.skipUnless(HAS_FF, "ffmpeg/ffprobe not installed")
    def test_speak_writes_measured_audio_and_receipt(self):
        out = self.tmp / "a.mp3"
        self.assertEqual(self.run_cli("speak", "صباح الفل", "--engine", "voicestudio", "--voice", "p1", "--out", str(out)), 0)
        rec = json.loads(Path(str(out) + ".receipt.json").read_text())
        self.assertEqual(rec["engine"], "voicestudio")
        self.assertEqual(rec["audio"]["codec"], "mp3")
        self.assertGreater(rec["audio"]["duration_s"], 0.4)
        sent = json.loads(Fake.seen[0][2])
        self.assertEqual((sent["voice"], sent["input"]), ("p1", "صباح الفل"))

    @unittest.skipUnless(HAS_FF, "ffmpeg/ffprobe not installed")
    def test_transcribe_writes_srt_and_words(self):
        audio = self.tmp / "in.wav"
        audio.write_bytes(tone_wav())
        out = self.tmp / "t.srt"
        self.assertEqual(self.run_cli("transcribe", str(audio), "--engine", "voicestudio", "--out", str(out)), 0)
        self.assertIn("صباح الفل", out.read_text())
        words = json.loads((self.tmp / "words.json").read_text())
        self.assertEqual(words[0], {"word": "صباح", "start": 0.0, "end": 0.5})  # overlap clipped

    @unittest.skipUnless(HAS_FF, "ffmpeg/ffprobe not installed")
    def test_clone_needs_consent_then_sends_multipart(self):
        ref = self.tmp / "me.wav"
        ref.write_bytes(tone_wav())
        self.assertEqual(self.run_cli("clone", str(ref), "--name", "King"), 2)
        self.assertEqual(Fake.seen, [])
        self.assertEqual(self.run_cli("clone", str(ref), "--name", "King", "--i-own-this-voice"), 0)
        path, ctype, body = Fake.seen[-1]
        self.assertEqual(path, "/api/profiles")
        self.assertTrue(ctype.startswith("multipart/form-data"))
        self.assertIn(b'name="kind"\r\n\r\nclone', body)
        self.assertIn(b'name="ref_audio"; filename="me.wav"', body)

    def test_design_maps_then_saves_and_refuses_unmapped(self):
        vs = vsm.VoiceStudio(self.url)
        r = vs.design("old man, deep voice", "Grandpa")
        self.assertEqual(r["profile"]["id"], "prof_1")
        self.assertIn(b'name="vd_states"\r\n\r\n{"Gender": "male", "Age": "elderly"}', Fake.seen[-1][2])
        with self.assertRaises(vsm.Fail):
            vs.design("a robot", "R")


if __name__ == "__main__":
    unittest.main()
