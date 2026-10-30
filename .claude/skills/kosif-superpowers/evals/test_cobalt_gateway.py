"""Offline Cobalt gateway tests. Never contact YouTube or public instances."""
from __future__ import annotations
import http.server
import json
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
import _cobalt_provider as cobalt

VIDEO_ID="dYrEeavC3cw"

class LocalCobalt(http.server.BaseHTTPRequestHandler):
    payload=b""
    mode="tunnel"
    body=None

    def log_message(self,*args): pass

    def do_POST(self):
        LocalCobalt.body=json.loads(self.rfile.read(int(self.headers.get("Content-Length","0"))))
        if self.mode=="error":
            data={"status":"error","error":{"code":"error.api.youtube.login"}}
        elif self.mode=="redirect":
            data={"status":"redirect","url":"https://another.example/media"}
        elif self.mode=="foreign":
            data={"status":"tunnel","url":"https://another.example/tunnel"}
        else:
            data={"status":"tunnel","url":f"http://127.0.0.1:{self.server.server_port}/tunnel?token=test"}
        out=json.dumps(data).encode()
        self.send_response(200);self.send_header("Content-Type","application/json");self.end_headers();self.wfile.write(out)

    def do_GET(self):
        self.send_response(200);self.send_header("Content-Type","video/mp4");self.end_headers()
        self.wfile.write(LocalCobalt.payload)


class CobaltGatewayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory()
        if shutil.which("ffmpeg"):
            movie=Path(cls.temp.name)/"fixture.mp4"
            subprocess.run(["ffmpeg","-hide_banner","-loglevel","error",
                            "-f","lavfi","-i","color=black:s=160x120:d=1:r=10",
                            "-c:v","mpeg4","-y",str(movie)],check=True,timeout=30)
            LocalCobalt.payload=movie.read_bytes()
        cls.server=http.server.ThreadingHTTPServer(("127.0.0.1",0),LocalCobalt)
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True)
        cls.thread.start()
        cls.api=f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown();cls.thread.join(timeout=5);cls.server.server_close();cls.temp.cleanup()

    def setUp(self): LocalCobalt.mode="tunnel"

    def test_id_forms(self):
        for u in [VIDEO_ID,"https://www.youtube.com/watch?v="+VIDEO_ID,
                  "https://youtu.be/"+VIDEO_ID,"https://youtube.com/shorts/"+VIDEO_ID]:
            self.assertEqual(cobalt.youtube_id(u),VIDEO_ID)

    def test_reject_domain_spoof(self):
        for u in ["https://fake-youtube.com/watch?v="+VIDEO_ID,
                  "https://youtube.com@evil.example/watch?v="+VIDEO_ID,"not-an-id"]:
            self.assertIsNone(cobalt.youtube_id(u))

    def test_reject_unsafe_endpoint(self):
        with self.assertRaises(cobalt.GatewayError): cobalt._endpoint(self.api)
        with self.assertRaises(cobalt.GatewayError):
            cobalt._endpoint("http://10.0.0.1:9876",allow_loopback=True)

    def test_rights_required(self):
        with self.assertRaises(cobalt.GatewayError):
            cobalt.download(VIDEO_ID,self.temp.name,self.api,rights="",allow_loopback=True)

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"),"ffmpeg and ffprobe required")
    def test_local_tunnel_real_verified_mp4(self):
        with tempfile.TemporaryDirectory() as path:
            receipt=cobalt.download(VIDEO_ID,path,self.api,rights="owned",allow_loopback=True)
            self.assertTrue(Path(receipt["file"]).is_file())
            self.assertTrue(receipt["verified"])
            self.assertEqual(receipt["width"],160)
            self.assertEqual(LocalCobalt.body["url"],"https://www.youtube.com/watch?v="+VIDEO_ID)

    def test_error_and_unsafe_redirect(self):
        for mode in ["error","redirect","foreign"]:
            LocalCobalt.mode=mode
            with tempfile.TemporaryDirectory() as path:
                with self.assertRaises(cobalt.GatewayError):
                    cobalt.download(VIDEO_ID,path,self.api,rights="owned",allow_loopback=True)
                self.assertFalse(list(Path(path).glob("*.mp4")))

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"),"ffmpeg and ffprobe required")
    def test_size_limit(self):
        with tempfile.TemporaryDirectory() as path:
            with self.assertRaises(cobalt.GatewayError):
                cobalt.download(VIDEO_ID,path,self.api,rights="owned",allow_loopback=True,max_bytes=100)
            self.assertFalse(list(Path(path).glob("*.mp4")))

if __name__=="__main__":
    unittest.main()
