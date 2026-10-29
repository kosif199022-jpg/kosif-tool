"""Offline tests for scripts/tiktok_photo.py (TikTok photo-post downloader).

No network: the page is the hand-written SYNTHETIC fixture evals/fixtures/tiktok_photo_minimal.html,
http_get and resolve_short are replaced by in-memory fakes, and yt-dlp is a fake script (YTDLP).
"""
from __future__ import annotations

import io
import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
FIXTURE = SKILL / "evals" / "fixtures" / "tiktok_photo_minimal.html"
sys.path.insert(0, str(SKILL / "scripts"))
import tiktok_photo as tp  # noqa: E402

PHOTO = "https://www.tiktok.com/@kosif.fixture/photo/7400000000000000001"
VIDEO = "https://www.tiktok.com/@kosif.fixture/video/7400000000000000001"
JPEG = b"\xff\xd8\xff\xe0" + b"\x00" * 60
WEBP = b"RIFF" + (60).to_bytes(4, "little") + b"WEBP" + b"\x00" * 52

FAKE_YTDLP = r'''#!/usr/bin/env python3
import os, sys
argv = sys.argv[1:]
log = os.environ.get("FAKE_YTDLP_LOG")
if log:
    with open(log, "a", encoding="utf-8") as f:
        f.write(" ".join(argv) + "\n")
tpl = argv[argv.index("-o") + 1]
with open(tpl.replace("%(ext)s", "m4a"), "wb") as f:
    f.write(b"fake-audio")
'''


def run(*argv) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        try:
            rc = tp.main(list(argv))
        except SystemExit as e:  # argparse
            rc = e.code
    return rc, out.getvalue(), err.getvalue()


def fixture_html() -> str:
    return FIXTURE.read_text(encoding="utf-8")


def with_json(mutate) -> str:
    """The fixture with its page JSON changed by mutate(data)."""
    html = fixture_html()
    data = tp.extract_universal_json(html)
    mutate(data)
    start = html.index('type="application/json">') + len('type="application/json">')
    end = html.index("</script>", start)
    return html[:start] + json.dumps(data, ensure_ascii=False) + html[end:]


def _to_video(d: dict) -> None:
    """Turn the fixture's photo post into a video post (no imagePost)."""
    item = d["__DEFAULT_SCOPE__"]["webapp.reflow.video.detail"]["itemInfo"]["itemStruct"]
    del item["imagePost"]
    item["video"] = {"duration": 12}


class Urls(unittest.TestCase):
    def test_photo_link_is_classified_and_rewritten(self):
        c = tp.classify_url(PHOTO + "?_r=1&_t=tracking")
        self.assertEqual((c["kind"], c["user"], c["id"]), ("photo", "kosif.fixture", "7400000000000000001"))
        self.assertEqual(c["photo_url"], PHOTO)
        self.assertEqual(c["video_url"], VIDEO)
        self.assertEqual(tp.rewrite_to_video(PHOTO + "/?lang=ar"), VIDEO)

    def test_video_short_foreign_and_other_links(self):
        self.assertEqual(tp.classify_url(VIDEO)["kind"], "video")
        for short in ("https://vt.tiktok.com/ZSabc123/", "https://vm.tiktok.com/ZMxyz/", "https://www.tiktok.com/t/ZTabc/",
                      "vt.tiktok.com/ZSabc123"):
            with self.subTest(short=short):
                c = tp.classify_url(short)
                self.assertEqual(c["kind"], "short")
                self.assertTrue(c["needs_resolve"])
        self.assertEqual(tp.classify_url("https://example.com/@a/photo/7400000000000000001")["kind"], "foreign")
        self.assertEqual(tp.classify_url("https://evil-tiktok.com/@a/photo/7400000000000000001")["kind"], "foreign")
        self.assertEqual(tp.classify_url("https://www.tiktok.com/@kosif.fixture")["kind"], "other")
        self.assertEqual(tp.classify_url("ftp://www.tiktok.com/@a/photo/1")["kind"], "invalid")
        with self.assertRaises(ValueError):
            tp.rewrite_to_video("https://vt.tiktok.com/ZSabc123/")

    def test_url_command(self):
        rc, out, _ = run("url", PHOTO + "?_r=1")
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out)["video_url"], VIDEO)
        self.assertEqual(run("url", "https://example.com/x")[0], 1)


class Parse(unittest.TestCase):
    def test_fixture_is_synthetic(self):
        hosts = {tp.urllib.parse.urlsplit(u).hostname for img in tp.extract_post(fixture_html())["images"] for u in img["urls"]}
        self.assertTrue(hosts and all(h.endswith(".invalid") for h in hosts), hosts)

    def test_parse_prints_the_post(self):
        rc, out, err = run("parse", str(FIXTURE))
        self.assertEqual(rc, 0, err)
        post = json.loads(out)
        self.assertEqual(post["author"], "kosif.fixture")
        self.assertEqual(post["music"]["title"], "original sound - kosif.fixture")
        self.assertIn("عرض صور", post["desc"])
        self.assertTrue(post["is_photo"])
        self.assertEqual(post["image_count"], 3)
        self.assertEqual([(i["width"], i["height"]) for i in post["images"]], [(1080, 1440), (1080, 1350), (720, 1280)])
        self.assertEqual(post["images"][0]["urls"][0], "https://img-a.example.invalid/slide0.jpeg?sig=fixture")  # / decoded
        self.assertEqual(len(post["images"][1]["urls"]), 2)
        self.assertEqual(post["photo_url"], PHOTO)
        self.assertEqual(post["video_url"], VIDEO)

    def _parse_text(self, html: str) -> tuple[int, str, str]:
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "page.html"
            p.write_text(html, encoding="utf-8")
            return run("parse", str(p))

    def test_missing_json_is_a_clear_error(self):
        rc, out, err = self._parse_text("<html><body>Log in to TikTok</body></html>")
        self.assertEqual(rc, 4)
        self.assertEqual(out, "")
        self.assertIn(tp.SCRIPT_ID, err)
        rc, _, err = self._parse_text('<script id="SIGI_STATE">{}</script>')
        self.assertEqual(rc, 4)
        self.assertIn("SIGI_STATE", err)
        rc, _, err = self._parse_text(f'<script id="{tp.SCRIPT_ID}" type="application/json">{{not json</script>')
        self.assertEqual(rc, 4)
        self.assertIn("does not parse", err)

    def test_removed_post_reports_the_status(self):
        def drop(d):
            d["__DEFAULT_SCOPE__"]["webapp.reflow.video.detail"] = {"statusCode": 10204, "itemInfo": {}}
        rc, _, err = self._parse_text(with_json(drop))
        self.assertEqual(rc, 4)
        self.assertIn("10204", err)

    def test_video_post_says_so_and_suggests_ytdlp(self):
        rc, out, err = self._parse_text(with_json(_to_video))
        self.assertEqual(rc, 3)
        self.assertFalse(json.loads(out)["is_photo"])
        self.assertIn("not a photo post", err)
        self.assertIn("yt-dlp", err)
        self.assertIn(VIDEO, err)

    def test_desktop_detail_key_is_a_fallback(self):
        def move(d):
            scope = d["__DEFAULT_SCOPE__"]
            scope["webapp.video-detail"] = scope.pop("webapp.reflow.video.detail")
        self.assertEqual(tp.extract_post(with_json(move))["image_count"], 3)


class Fetch(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.out = self.dir / "post"
        self.calls: list[str] = []
        self.fail_hosts: set[str] = set()
        self.not_image: set[str] = set()
        self.video_page = ""
        fake = self.dir / "fake-yt-dlp"
        fake.write_text(FAKE_YTDLP, encoding="utf-8")
        fake.chmod(fake.stat().st_mode | stat.S_IXUSR)
        self.ytlog = self.dir / "ytdlp.log"
        self._env = {k: os.environ.get(k) for k in ("YTDLP", "FAKE_YTDLP_LOG")}
        os.environ["YTDLP"] = str(fake)
        os.environ["FAKE_YTDLP_LOG"] = str(self.ytlog)
        self._saved = (tp.http_get, tp.resolve_short, tp.PAUSE)
        tp.http_get = self.fake_get
        tp.resolve_short = self.fake_resolve
        tp.PAUSE = 0

    def tearDown(self):
        tp.http_get, tp.resolve_short, tp.PAUSE = self._saved
        for k, v in self._env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        self.tmp.cleanup()

    def fake_get(self, url, referer=None, limit=tp.PAGE_LIMIT, timeout=30):
        self.calls.append(url)
        host = tp.urllib.parse.urlsplit(url).hostname
        if url == PHOTO:
            return fixture_html().encode("utf-8")
        if url == VIDEO:
            return self.video_page.encode("utf-8")
        if host in self.fail_hosts or any(s in url for s in self.fail_hosts):
            raise tp.FetchError("HTTP 403 for " + host)
        if any(s in url for s in self.not_image):
            return b"<html>blocked</html>"
        self.assertEqual(referer, PHOTO)
        return WEBP if url.split("?")[0].endswith(".webp") else JPEG

    def fake_resolve(self, url, timeout=20):
        self.calls.append("resolve:" + url)
        return PHOTO

    def meta(self) -> dict:
        return json.loads((self.out / "meta.json").read_text(encoding="utf-8"))

    def test_fetch_from_saved_page_writes_images_audio_and_meta(self):
        rc, out, err = run("fetch", PHOTO + "?_r=1", "--out", str(self.out), "--html", str(FIXTURE))
        self.assertEqual(rc, 0, err)
        names = sorted(p.name for p in self.out.iterdir())
        self.assertEqual(names, ["audio.m4a", "img00.jpg", "img01.jpg", "img02.webp", "meta.json"])
        m = self.meta()
        self.assertEqual(json.loads(out), m)
        self.assertEqual(m["schema"], "kosif.tiktok_photo.v1")
        self.assertEqual(m["source_url"], PHOTO)  # tracking query removed
        self.assertEqual(m["author"]["unique_id"], "kosif.fixture")
        self.assertEqual(m["music"]["title"], "original sound - kosif.fixture")
        self.assertIn("Synthetic slideshow", m["desc"])
        self.assertEqual([(i["file"], i["width"], i["height"]) for i in m["images"]],
                         [("img00.jpg", 1080, 1440), ("img01.jpg", 1080, 1350), ("img02.webp", 720, 1280)])
        self.assertTrue(all(len(i["sha256"]) == 64 and i["bytes"] > 0 for i in m["images"]))
        self.assertNotIn("sig=fixture", json.dumps(m))  # signed CDN links are not kept
        self.assertTrue(m["complete"])
        self.assertEqual(m["audio"]["file"], "audio.m4a")
        self.assertIn("@kosif.fixture", m["credit"])
        log = self.ytlog.read_text(encoding="utf-8")
        self.assertIn("-f ba", log)
        self.assertTrue(log.strip().endswith("-- " + VIDEO), log)  # the rewritten /video/ link

    def test_short_link_is_resolved_then_fetched(self):
        rc, _, err = run("fetch", "https://vt.tiktok.com/ZSfixture1/", "--out", str(self.out), "--no-audio")
        self.assertEqual(rc, 0, err)
        self.assertEqual(self.calls[:2], ["resolve:https://vt.tiktok.com/ZSfixture1/", PHOTO])
        m = self.meta()
        self.assertEqual(m["source_url"], "https://vt.tiktok.com/ZSfixture1/")
        self.assertEqual(m["resolved_url"], PHOTO)
        self.assertTrue(m["audio"]["skipped"])
        self.assertFalse(self.ytlog.exists())

    def test_video_post_is_refused_with_a_ytdlp_hint(self):
        self.video_page = with_json(_to_video)
        rc, _, err = run("fetch", VIDEO, "--out", str(self.out))
        self.assertEqual(rc, 3)
        self.assertIn("not a photo post", err)
        self.assertIn("yt-dlp", err)
        self.assertEqual(self.calls, [VIDEO])  # only the page was read
        self.assertFalse(self.out.exists())

    def test_video_link_to_a_slideshow_still_downloads(self):
        self.video_page = fixture_html()
        rc, _, err = run("fetch", VIDEO + "?is_from_webapp=1", "--out", str(self.out), "--no-audio")
        self.assertEqual(rc, 0, err)
        self.assertEqual(self.meta()["image_count"], 3)

    def test_foreign_link_is_refused(self):
        rc, _, err = run("fetch", "https://example.com/@a/photo/7400000000000000001", "--out", str(self.out))
        self.assertEqual(rc, 1)
        self.assertIn("not a TikTok link", err)
        self.assertEqual(self.calls, [])

    def test_partial_download_is_reported_then_resumed(self):
        self.fail_hosts = {"slide1"}  # both mirrors of image 1 fail
        rc, _, err = run("fetch", PHOTO, "--out", str(self.out))
        self.assertEqual(rc, 2, err)
        self.assertIn("partial download", err)
        m = self.meta()
        self.assertFalse(m["complete"])
        self.assertEqual(m["failed"], [1])
        self.assertEqual(m["downloaded"], 2)
        self.assertIn("403", m["images"][1]["error"])
        self.assertEqual(sum("slide1" in c for c in self.calls), 2 * tp.ATTEMPTS)  # each mirror retried
        self.assertFalse(list(self.out.glob("*.part")))
        self.assertFalse(list(self.out.glob("img01.*")))
        # rerun: only the missing image is fetched again
        self.fail_hosts, self.calls = set(), []
        rc, _, err = run("fetch", PHOTO, "--out", str(self.out))
        self.assertEqual(rc, 0, err)
        self.assertEqual([c for c in self.calls if "example.invalid" in c], ["https://img-a.example.invalid/slide1.jpeg?sig=fixture"])
        m = self.meta()
        self.assertTrue(m["complete"])
        self.assertTrue(m["images"][0]["resumed"])
        self.assertTrue(m["audio"]["resumed"])

    def test_mirror_is_used_when_the_first_link_fails(self):
        self.fail_hosts = {"img-a.example.invalid"}
        rc, _, _ = run("fetch", PHOTO, "--out", str(self.out), "--no-audio")
        self.assertEqual(rc, 2)
        m = self.meta()
        self.assertEqual(m["failed"], [0, 2])  # only image 1 has a second mirror
        self.assertTrue(m["images"][1]["ok"])

    def test_an_html_answer_is_not_saved_as_an_image(self):
        self.not_image = {"slide2"}
        rc, _, _ = run("fetch", PHOTO, "--out", str(self.out), "--no-audio")
        self.assertEqual(rc, 2)
        m = self.meta()
        self.assertEqual(m["failed"], [2])
        self.assertIn("not an image", m["images"][2]["error"])

    def test_missing_ytdlp_keeps_the_images(self):
        os.environ["YTDLP"] = str(self.dir / "no-such-yt-dlp")
        rc, _, err = run("fetch", PHOTO, "--out", str(self.out))
        self.assertEqual(rc, 2)
        m = self.meta()
        self.assertEqual(m["failed"], [])
        self.assertFalse(m["audio"]["ok"])
        self.assertIn("audio failed", err)

    def test_max_images_cap(self):
        rc, _, _ = run("fetch", PHOTO, "--out", str(self.out), "--no-audio", "--max-images", "2")
        self.assertEqual(rc, 0)
        self.assertEqual(self.meta()["image_count"], 2)
        self.assertFalse(list(self.out.glob("img02.*")))


class Cli(unittest.TestCase):
    def test_help_and_bad_args(self):
        proc = subprocess.run([sys.executable, str(SKILL / "scripts" / "tiktok_photo.py"), "--help"],
                              capture_output=True, text=True, timeout=60)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        for word in ("fetch", "parse", "url"):
            self.assertIn(word, proc.stdout)
        self.assertEqual(run("fetch", "--out", "x")[0], 1)  # neither a link nor --html

    def test_usage_errors_exit_1_never_2_which_means_partial_download(self):
        script = str(SKILL / "scripts" / "tiktok_photo.py")
        for argv in (["fetch", "https://www.tiktok.com/@a/photo/7400000000000000001"],   # missing --out
                     ["fetch", "x", "--max-images", "abc", "--out", "/nonexistent"],      # not an integer
                     ["fetch", "x", "--out", "y", "--unknown-flag"],
                     ["nope"], []):
            proc = subprocess.run([sys.executable, script, *argv], capture_output=True, text=True, timeout=60)
            self.assertEqual(proc.returncode, 1, (argv, proc.stderr))
            self.assertIn("error:", proc.stderr)
            self.assertIn("usage:", proc.stderr)
            self.assertEqual(run(*argv)[0], 1, argv)
        for argv in (["--help"], ["fetch", "--help"], ["url", "--help"]):
            self.assertEqual(run(*argv)[0], 0, argv)

    def test_http_get_refuses_plain_http_before_connecting(self):
        with self.assertRaises(tp.FetchError):
            tp.http_get("http://www.tiktok.com/@a/photo/7400000000000000001")

    def test_sniff_ext(self):
        self.assertEqual(tp.sniff_ext(JPEG), "jpg")
        self.assertEqual(tp.sniff_ext(WEBP), "webp")
        self.assertEqual(tp.sniff_ext(b"\x89PNG\r\n\x1a\n" + b"\x00" * 8), "png")
        self.assertIsNone(tp.sniff_ext(b"<html>"))


if __name__ == "__main__":
    unittest.main()
