"""song_preview.py: official store previews as the DRM fallback; HTTP is mocked, no network in these tests."""
from __future__ import annotations

import io
import json
import subprocess
import sys
import tempfile
import unittest
import urllib.error
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / ".claude" / "skills" / "kosif-superpowers" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import song_preview as sp  # noqa: E402

ITUNES = {"resultCount": 1, "results": [{
    "kind": "song", "trackId": 111, "artistId": 222, "collectionId": 333,
    "trackName": "انا بحبك يا بلادي", "artistName": "Tamer Ashour", "collectionName": "Single",
    "releaseDate": "2026-10-01T12:00:00Z", "trackTimeMillis": 215000,
    "previewUrl": "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview/x/mzaf_1.plus.aac.p.m4a",
    "trackViewUrl": "https://music.apple.com/eg/album/x/333?i=111"}]}
DEEZER = {"data": [
    {"type": "track", "id": 9, "title": "Ana Bahebek Ya Blady", "duration": 214, "preview": "",
     "link": "https://www.deezer.com/track/9", "artist": {"id": 8, "name": "Tamer Ashour"}, "album": {"id": 7, "title": "Single"}},
    {"type": "track", "id": 10, "title": "Other", "duration": 200,
     "preview": "https://cdnt-preview.dzcdn.net/api/1/1/a/b/c/0/abc.mp3?hdnea=exp=1",
     "link": "https://www.deezer.com/track/10", "artist": {"id": 8, "name": "Tamer Ashour"}, "album": {"id": 6, "title": "Album"}}]}
AUDIO = b"\x00\x00\x00\x20ftypM4A fake preview bytes"


def fake_fetch(url, **kw):
    if url.startswith("https://itunes.apple.com/search"):
        return json.dumps(ITUNES).encode()
    if url.startswith("https://api.deezer.com/search"):
        return json.dumps(DEEZER).encode()
    if "itunes.apple.com/itunes-assets" in url or "dzcdn.net" in url:
        return AUDIO
    raise AssertionError(f"unexpected URL {url}")


class Resp(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


class SongPreviewTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.out = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def run_main(self, *argv):
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = sp.main(list(argv))
        return code, buf.getvalue()

    def test_parsers_normalise_both_sources(self):
        it = sp.parse_itunes(ITUNES)[0]
        self.assertEqual((it["source"], it["duration_s"], it["release_date"], it["track_id"]), ("itunes", 215, "2026-10-01", 111))
        dz = sp.parse_deezer(DEEZER)
        self.assertIsNone(dz[0]["preview_url"])        # Deezer's preview field is sometimes empty
        self.assertEqual(dz[0]["artist_id"], 8)
        self.assertIn("country=eg", sp.itunes_url("x", "eg", 10))
        self.assertIn("entity=song", sp.itunes_url("x", "eg", 10))

    def test_search_prints_rows_and_saves_cache(self):
        with mock.patch.object(sp, "fetch", side_effect=fake_fetch):
            code, out = self.run_main("search", "Tamer Ashour انا بحبك يا بلادي", "--out", str(self.out))
        self.assertEqual(code, 0)
        self.assertIn("itunes", out)
        self.assertIn("deezer", out)
        cache = json.loads((self.out / sp.CACHE_NAME).read_text(encoding="utf-8"))
        self.assertEqual(cache["schema"], sp.RESULTS_SCHEMA)
        self.assertEqual([r["n"] for r in cache["rows"]], [1, 2, 3])

    def test_search_json_and_one_source_failing(self):
        def half(url, **kw):
            if "deezer" in url:
                raise sp.FetchError("HTTP 503: deezer")
            return fake_fetch(url)
        with mock.patch.object(sp, "fetch", side_effect=half):
            code, out = self.run_main("search", "x", "--json", "--out", str(self.out))
        payload = json.loads(out)
        self.assertEqual(code, 0)
        self.assertIn("deezer", payload["errors"])
        self.assertEqual(len(payload["rows"]), 1)

    def test_download_row_writes_preview_and_rights_sidecar(self):
        with mock.patch.object(sp, "fetch", side_effect=fake_fetch):
            self.run_main("search", "Tamer Ashour", "--out", str(self.out))
            with mock.patch.object(sp, "ffprobe_duration", return_value=30.0):
                code, out = self.run_main("download", "1", "--out", str(self.out))
        self.assertEqual(code, 0)
        files = sorted(p.name for p in self.out.iterdir())
        audio = [f for f in files if f.endswith(".m4a")]
        self.assertEqual(len(audio), 1)
        self.assertEqual((self.out / audio[0]).read_bytes(), AUDIO)
        rights = json.loads((self.out / (audio[0] + ".rights.json")).read_text(encoding="utf-8"))
        for key in ("source", "track_id", "artist_id", "store_url", "preview_url", "fetched_at", "licence_note"):
            self.assertIn(key, rights)
        self.assertEqual(rights["track_id"], 111)
        self.assertIn("official 30 s store preview", rights["licence_note"])
        self.assertIn("TikTok library", rights["licence_note"])
        self.assertIn("credit artist", rights["licence_note"])
        self.assertEqual(rights["duration_s"], 30.0)
        self.assertIn("duration 30.0 s", out)

    def test_download_deezer_row_is_mp3(self):
        with mock.patch.object(sp, "fetch", side_effect=fake_fetch):
            self.run_main("search", "x", "--out", str(self.out))
            with mock.patch.object(sp, "ffprobe_duration", return_value=None):
                code, out = self.run_main("download", "3", "--out", str(self.out))
        self.assertEqual(code, 0)
        self.assertTrue(any(p.suffix == ".mp3" for p in self.out.iterdir()))
        self.assertIn("ffprobe not available", out)

    def test_row_without_preview_and_foreign_hosts_are_refused(self):
        with mock.patch.object(sp, "fetch", side_effect=fake_fetch):
            self.run_main("search", "x", "--out", str(self.out))
            with self.assertRaises(SystemExit):
                sp.main(["download", "2", "--out", str(self.out)])     # Deezer row with an empty preview
        for url in ("https://soundcloud.com/a/b", "http://audio-ssl.itunes.apple.com/x.m4a",
                    "https://evil.example/itunes.apple.com.m4a", "https://media.example.com/stream.m3u8"):
            self.assertFalse(sp.allowed_preview_url(url), url)
            with mock.patch.object(sp, "fetch") as f, self.assertRaises(SystemExit):
                sp.main(["download", url, "--out", str(self.out)])
            f.assert_not_called()
        self.assertTrue(sp.allowed_preview_url("https://audio-ssl.itunes.apple.com/a.m4a"))
        self.assertTrue(sp.allowed_preview_url("https://cdnt-preview.dzcdn.net/a.mp3"))

    def test_download_without_a_search_is_explained(self):
        with self.assertRaises(SystemExit) as cm:
            sp.main(["download", "1", "--out", str(self.out / "empty")])
        self.assertIn("search", str(cm.exception))

    def test_fetch_retries_are_limited_and_4xx_is_not_retried(self):
        calls = []

        def boom(req, timeout):
            calls.append(timeout)
            raise urllib.error.URLError("proxy reset")
        with mock.patch.object(sp.urllib.request, "urlopen", side_effect=boom), mock.patch.object(sp.time, "sleep"):
            with self.assertRaises(sp.FetchError):
                sp.fetch("https://itunes.apple.com/search?term=x", timeout=5, retries=2)
        self.assertEqual(calls, [5, 5, 5])

        calls.clear()

        def not_found(req, timeout):
            calls.append(1)
            raise urllib.error.HTTPError(req.full_url, 404, "nf", {}, None)
        with mock.patch.object(sp.urllib.request, "urlopen", side_effect=not_found), mock.patch.object(sp.time, "sleep"):
            with self.assertRaises(sp.FetchError):
                sp.fetch("https://itunes.apple.com/x", retries=3)
        self.assertEqual(len(calls), 1)

        with mock.patch.object(sp.urllib.request, "urlopen", return_value=Resp(b"x" * 11)):
            with self.assertRaises(sp.FetchError):
                sp.fetch("https://itunes.apple.com/x", max_bytes=10)

    def test_help_is_bilingual_and_tool_stays_lawful(self):
        p = subprocess.run([sys.executable, str(SCRIPTS / "song_preview.py"), "--help"], capture_output=True, text=True, timeout=60)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("DRM", p.stdout)
        self.assertIn("معاينة", p.stdout)
        src = (SCRIPTS / "song_preview.py").read_text(encoding="utf-8")
        self.assertNotIn("import yt_dlp", src)
        self.assertNotIn("cookiejar", src)


if __name__ == "__main__":
    unittest.main()
