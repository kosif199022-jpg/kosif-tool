"""Stream grabber: DASH/HLS layouts made by ffmpeg, served on loopback, grabbed and decoded; protected streams refused."""
import functools, http.server, os, shutil, subprocess, sys, tempfile, threading, unittest
from pathlib import Path
SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK / "scripts"))
import stream_grabber as G  # noqa: E402

HAVE = bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))


def ff(*args, cwd):
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *args], cwd=cwd, check=True)


@unittest.skipUnless(HAVE, "ffmpeg/ffprobe not installed")
class StreamGrabberTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["NO_PROXY"] = os.environ["no_proxy"] = "127.0.0.1,localhost"
        cls.tmp = Path(tempfile.mkdtemp())
        srv = cls.tmp / "srv"
        src = cls.tmp / "src.mp4"
        ff("-f", "lavfi", "-i", "testsrc2=size=320x180:rate=25:duration=6", "-f", "lavfi", "-i", "sine=frequency=440:duration=6",
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-g", "25", "-c:a", "aac", "-shortest", str(src), cwd=cls.tmp)
        layouts = {
            "tl": ["-map", "0:v", "-map", "0:a", "-c", "copy", "-f", "dash", "-seg_duration", "1", "-use_template", "1", "-use_timeline", "1", "m.mpd"],
            "num": ["-map", "0:v", "-map", "0:a", "-c", "copy", "-f", "dash", "-seg_duration", "1", "-use_template", "1", "-use_timeline", "0", "m.mpd"],
            "single": ["-map", "0:v", "-map", "0:a", "-c", "copy", "-f", "dash", "-single_file", "1", "m.mpd"],
            "ts": ["-c", "copy", "-f", "hls", "-hls_time", "1", "-hls_playlist_type", "vod", "i.m3u8"],
            "fmp4": ["-c", "copy", "-f", "hls", "-hls_time", "1", "-hls_segment_type", "fmp4", "-hls_playlist_type", "vod", "i.m3u8"],
            "br": ["-c", "copy", "-f", "hls", "-hls_time", "1", "-hls_flags", "single_file", "-hls_playlist_type", "vod", "i.m3u8"],
        }
        for name, args in layouts.items():
            d = srv / name
            d.mkdir(parents=True)
            ff("-i", str(src), *args, cwd=d)
        enc = srv / "enc"
        enc.mkdir()
        (enc / "k.key").write_bytes(os.urandom(16))
        (enc / "ki").write_text("k.key\nk.key\n")
        ff("-i", str(src), "-c", "copy", "-f", "hls", "-hls_time", "1", "-hls_key_info_file", "ki", "-hls_playlist_type", "vod", "i.m3u8", cwd=enc)
        drm = srv / "drm"
        drm.mkdir()
        (drm / "m.mpd").write_text((srv / "tl" / "m.mpd").read_text().replace("<Representation ", '<ContentProtection schemeIdUri="urn:mpeg:dash:mp4protection:2011"/><Representation ', 1))
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(srv))
        handler.log_message = lambda *a, **k: None
        cls.httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        threading.Thread(target=cls.httpd.serve_forever, daemon=True).start()
        cls.base = f"http://127.0.0.1:{cls.httpd.server_address[1]}/"

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def grab_ok(self, path):
        out = self.tmp / (path.replace("/", "_") + ".mp4")
        r = G.grab(self.base + path, out, threads=4, work=self.tmp / ("w_" + path.replace("/", "_")))
        dur = float(r["probe"]["format"]["duration"])
        self.assertAlmostEqual(dur, 6.0, delta=0.15, msg=path)
        errs = subprocess.run(["ffmpeg", "-v", "error", "-i", str(out), "-f", "null", "-"], capture_output=True, text=True).stderr
        self.assertEqual(errs.strip(), "", path)
        kinds = {s["codec_type"] for s in r["probe"]["streams"]}
        self.assertEqual(kinds, {"video", "audio"}, path)

    def test_dash_timeline(self):
        self.grab_ok("tl/m.mpd")

    def test_dash_number_template_probes_tail(self):
        self.grab_ok("num/m.mpd")

    def test_dash_single_file_ranges_on_server_without_range_support(self):
        self.grab_ok("single/m.mpd")

    def test_hls_ts(self):
        self.grab_ok("ts/i.m3u8")

    def test_hls_fmp4(self):
        self.grab_ok("fmp4/i.m3u8")

    def test_hls_byterange(self):
        self.grab_ok("br/i.m3u8")

    def test_encrypted_and_drm_refused(self):
        for p in ("enc/i.m3u8", "drm/m.mpd"):
            with self.assertRaises(G.Refused, msg=p):
                G.list_tracks(self.base + p)

    def test_find_streams_in_saved_page_and_har(self):
        page = self.tmp / "page.html"
        page.write_text('<script>var c={"hls":"https:\\/\\/cdn.x\\/a\\/m.m3u8?t=1"}</script><video src="https://cdn.x/b.mp4"></video>', encoding="utf-8")
        found = G.find_streams(str(page))
        self.assertEqual([f["kind"] for f in found], ["manifest", "file"])
        self.assertEqual(found[0]["url"], "https://cdn.x/a/m.m3u8?t=1")
        har = self.tmp / "c.har"
        har.write_text('{"log":{"entries":[{"request":{"url":"https://cdn.y/v/seg"},"response":{"headers":[{"name":"Content-Type","value":"application/dash+xml"}]}}]}}')
        self.assertEqual(G.find_streams(str(har))[0]["url"], "https://cdn.y/v/seg")

    def test_pick_prefers_editable_codecs_at_same_height(self):
        tr = [{"type": "video", "height": 1080, "bandwidth": 5_000_000, "codecs": "av01.0.08M.08", "id": "av1"},
              {"type": "video", "height": 1080, "bandwidth": 4_000_000, "codecs": "avc1.640028", "id": "h264"},
              {"type": "video", "height": 2160, "bandwidth": 9_000_000, "codecs": "avc1.640033", "id": "4k"},
              {"type": "audio", "height": 0, "bandwidth": 128000, "codecs": "mp4a.40.2", "id": "aac"}]
        v, a = G.pick(tr, max_height=1080)
        self.assertEqual((v["id"], a["id"]), ("h264", "aac"))
        self.assertEqual(G.pick(tr, max_height=1080, prefer="quality")[0]["id"], "av1")
        self.assertIn("1080p · avc1", G.label(v))

    def test_container_and_vtt_merge(self):
        self.assertEqual(G.container_for({"codecs": "vp8"}, {"codecs": "vorbis"}), ".mkv")
        self.assertEqual(G.container_for({"codecs": "avc1.64001f"}, {"codecs": "mp4a.40.2"}), ".mp4")
        m = G.merge_vtt([b"WEBVTT\n\n00:00.000 --> 00:01.000\nA\n", b"WEBVTT\nX-TIMESTAMP-MAP=MPEGTS:0\n\n00:01.000 --> 00:02.000\nB\n"]).decode()
        self.assertEqual(m.count("WEBVTT"), 1)
        self.assertNotIn("X-TIMESTAMP-MAP", m)
        self.assertIn("A", m)
        self.assertIn("B", m)

    def test_cookie_header_refused(self):
        self.assertEqual(G.main(["--header", "Cookie: s=1", "list", "x"]), 3)

    def test_template_formatting(self):
        self.assertEqual(G.tpl("seg-$RepresentationID$-$Number%05d$.m4s", "v1", "800", number=7), "seg-v1-00007.m4s")
        self.assertEqual(G.tpl("t$Time$-$$", "a", "1", time=9000), "t9000-$")
        self.assertAlmostEqual(G.iso_dur("PT1M2.5S"), 62.5)


if __name__ == "__main__":
    unittest.main()
