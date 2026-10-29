"""Source finder, offline: cut detection, ORB+RANSAC verification, Yandex answer parsing, the captcha stop,
the rate limit and the whole run chain. Every network call is replaced by a fake; nothing leaves the machine."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SK = Path(__file__).resolve().parents[1]
SCRIPT = SK / "scripts" / "source_finder.py"
sys.path.insert(0, str(SK / "scripts"))
import source_finder as S  # noqa: E402

try:
    import cv2
    import numpy as np
    HAVE_CV = True
except ImportError:  # pragma: no cover
    HAVE_CV = False
HAVE_FF = bool(shutil.which("ffmpeg"))

UPLOAD_OK = json.dumps({"blocks": [{"block": "b-page_type_search-by-image__link",
                                     "params": {"url": "cbir_id=4567%2Fabc&rpt=imageview", "cbirId": "4567/abc"}}]})
SITES_PAGE = ("<html><body>" + "x" * 70000 +
              '<a href="https://www.pinterest.com/pin/123456789012/">pin</a>'
              '<div data-state="{&quot;url&quot;:&quot;https://ru.pinterest.com/pin/some-title--987654321/&quot;}"></div>'
              '<script>{"u":"https:\\/\\/pinterest.com\\/pin\\/555555555\\/"}</script>'
              '<a href="https://www.pinterest.com/pin/123456789012/">duplicate</a>'
              '<a href="https://www.pinterest.com/someone/boards/">a board, not a pin</a>'
              '<a href="https://www.tiktok.com/@maker/video/7300000000000000000">tiktok</a>'
              '<a href="https://yandex.com/images/search?text=pexels.com">yandex self link</a>'
              "<p>the word captcha deep inside a big normal page</p></body></html>")
SIMILAR_PAGE = "<html>" + "y" * 70000 + '<img src="https://i.pinimg.com/x.jpg"><a href="https://www.pinterest.com/pin/777777777/">p</a></html>'
CAPTCHA_PAGE = '<html><form action="/checkcaptcha"><div class="SmartCaptcha">Are you a robot?</div></form></html>'


def no_network(*_a, **_k):
    raise AssertionError("a test tried to reach the network")


# ----------------------------------------------------------------------------------------- synthetic media

def scene(seed, w=640, h=360):
    """A textured synthetic 'shot': flat background, 45 random shapes and 6 random words."""
    rng = np.random.default_rng(seed)
    img = np.empty((h, w, 3), np.uint8)
    img[:] = rng.integers(30, 220, 3)
    for _ in range(45):
        c = tuple(int(x) for x in rng.integers(0, 256, 3))
        k = rng.integers(0, 3)
        x, y = int(rng.integers(0, w)), int(rng.integers(0, h))
        if k == 0:
            cv2.rectangle(img, (x, y), (x + int(rng.integers(10, 120)), y + int(rng.integers(10, 90))), c, -1)
        elif k == 1:
            cv2.circle(img, (x, y), int(rng.integers(5, 50)), c, -1)
        else:
            cv2.line(img, (x, y), (int(rng.integers(0, w)), int(rng.integers(0, h))), c, int(rng.integers(1, 5)))
    for _ in range(6):
        cv2.putText(img, "".join(chr(int(v)) for v in rng.integers(65, 91, 5)),
                    (int(rng.integers(0, w - 150)), int(rng.integers(30, h))), cv2.FONT_HERSHEY_SIMPLEX,
                    float(rng.uniform(0.6, 1.4)), tuple(int(x) for x in rng.integers(0, 256, 3)), 2)
    return img


def warp(img, seed=7):
    """The same picture through a random perspective homography (up to 6 % per corner) plus Gaussian noise."""
    rng = np.random.default_rng(seed)
    h, w = img.shape[:2]
    src = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
    dst = (src + rng.uniform(-0.06, 0.06, (4, 2)) * [w, h]).astype(np.float32)
    out = cv2.warpPerspective(img, cv2.getPerspectiveTransform(src, dst), (w, h), borderMode=cv2.BORDER_REFLECT)
    return np.clip(out.astype(np.int16) + rng.normal(0, 6, out.shape).astype(np.int16), 0, 255).astype(np.uint8)


def write_video(path, frames, fps=10):
    h, w = frames[0].shape[:2]
    vw = cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*"MJPG"), fps, (w, h))
    if not vw.isOpened():
        raise unittest.SkipTest("OpenCV cannot write MJPG/AVI here")
    for f in frames:
        vw.write(f)
    vw.release()
    return path


def moving(img, n, dx=2):
    """n frames of one shot with a small pan, so in-shot motion must not count as a cut."""
    return [np.roll(img, i * dx, axis=1) for i in range(n)]


# --------------------------------------------------------------------------------------------- tests

class HelpWithoutOpenCV(unittest.TestCase):
    BLOCK = ("import runpy, sys\n"
             "class B:\n"
             "    def find_spec(self, name, path=None, target=None):\n"
             "        if name.split('.')[0] in ('cv2', 'numpy'):\n"
             "            raise ImportError('blocked ' + name)\n"
             "sys.meta_path.insert(0, B())\n"
             "sys.argv = sys.argv[1:]\n"
             "runpy.run_path(sys.argv[0], run_name='__main__')\n")

    def call(self, *args):
        return subprocess.run([sys.executable, "-c", self.BLOCK, str(SCRIPT), *args], capture_output=True, text=True)

    def test_help_and_every_subcommand_help_work_without_cv2_numpy(self):
        for args in (["--help"], ["cuts", "-h"], ["frames", "-h"], ["search", "-h"], ["match", "-h"], ["run", "-h"],
                     ["doctor", "-h"]):
            r = self.call(*args)
            self.assertEqual(r.returncode, 0, (args, r.stderr))
            self.assertIn("usage", r.stdout)

    def test_cv_command_without_cv2_says_how_to_install(self):
        with tempfile.TemporaryDirectory() as d:
            video = Path(d) / "v.mp4"
            video.write_bytes(b"\0")
            r = self.call("cuts", str(video))
        self.assertEqual(r.returncode, 1)
        self.assertIn("opencv-python-headless", r.stderr)


class SearchParsingOffline(unittest.TestCase):
    def setUp(self):
        S._LAST_CALL[0] = 0.0
        self.tmp = Path(tempfile.mkdtemp())
        self.img = self.tmp / "q.jpg"
        self.img.write_bytes(b"\xff\xd8 not really a jpeg; never uploaded")
        p = mock.patch.object(S.time, "sleep", lambda s: None)
        p.start()
        self.addCleanup(p.stop)
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def test_parse_upload(self):
        self.assertEqual(S.parse_upload(UPLOAD_OK), "4567/abc")
        self.assertEqual(S.parse_upload('{"blocks":[{"params":{"url":"cbir_id=9%2Fz&x=1"}}]}'), "9/z")
        with self.assertRaises(S.CaptchaError):
            S.parse_upload('{"type":"captcha","captcha":{"img-url":"https://x/y"}}')
        with self.assertRaises(S.CaptchaError):
            S.parse_upload(CAPTCHA_PAGE)
        with self.assertRaises(S.SourceFinderError) as cm:
            S.parse_upload("<html>a redesigned page</html>")
        self.assertNotIsInstance(cm.exception, S.CaptchaError)

    def test_extract_links_finds_pins_in_every_encoding_once(self):
        got = S.extract_links(SITES_PAGE)
        self.assertEqual(got["pins"], ["123456789012", "987654321", "555555555"])
        self.assertEqual(len(got["pinterest"]), 3)
        self.assertEqual(got["leads"], ["https://www.tiktok.com/@maker/video/7300000000000000000"])

    def test_captcha_page_detection(self):
        self.assertTrue(S.page_is_captcha(CAPTCHA_PAGE))
        self.assertFalse(S.page_is_captcha(SITES_PAGE))       # big normal page that merely mentions the word

    def test_search_collects_pins_from_both_pages(self):
        with mock.patch.object(S, "_curl", side_effect=[UPLOAD_OK, SITES_PAGE, SIMILAR_PAGE]) as c:
            r = S.yandex_search(self.img)
        self.assertEqual(c.call_count, 3)
        self.assertEqual(r["cbir_id"], "4567/abc")
        self.assertEqual(r["pins"], ["123456789012", "987654321", "555555555", "777777777"])
        self.assertEqual(set(r["pages"]), {"sites", "similar"})
        page_url = c.call_args_list[1][0][0][0]
        self.assertIn("cbir_page=sites", page_url)
        self.assertIn("cbir_id=4567%2Fabc", page_url)

    def test_captcha_stops_every_further_call(self):
        with mock.patch.object(S, "_curl", side_effect=[UPLOAD_OK, CAPTCHA_PAGE, SIMILAR_PAGE]) as c:
            with self.assertRaises(S.CaptchaError):
                S.yandex_search(self.img)
        self.assertEqual(c.call_count, 2)

    def test_search_cli_exits_3_on_captcha_after_one_upload(self):
        second = self.tmp / "q2.jpg"
        second.write_bytes(b"x")
        with mock.patch.object(S, "_curl", side_effect=['{"type":"captcha"}', UPLOAD_OK]) as c:
            code = S.main(["search", str(self.img), str(second), "--out", str(self.tmp / "s.json")])
        self.assertEqual(code, 3)
        self.assertEqual(c.call_count, 1)
        self.assertEqual(json.loads((self.tmp / "s.json").read_text()), [])

    def test_search_cache_is_keyed_by_the_image_bytes_not_its_name(self):
        calls = []

        def fake_search(image, pages=S.PAGES, delay=4.0):
            body = Path(image).read_bytes().decode()
            calls.append(body)
            return {"image": str(image), "cbir_id": "x", "pages": {p: {} for p in pages}, "pins": [f"pins-for-{body}"],
                    "pinterest": [], "leads": []}

        q = self.tmp / "queries" / "s003_0.jpg"
        q.parent.mkdir()
        cache = self.tmp / "search"
        # a cache file in the old name-only format must not be served for a new frame
        cache.mkdir()
        (cache / "s003_0.json").write_text(json.dumps({"pages": {"sites": {}, "similar": {}}, "pins": ["stale"]}))
        with mock.patch.object(S, "yandex_search", fake_search), mock.patch.object(S, "_curl", no_network):
            q.write_bytes(b"crop-A")
            first = S.cached_search(q, cache)
            q.write_bytes(b"crop-B")                     # rerun with another --crop: same name, new frame
            second = S.cached_search(q, cache)
            q.write_bytes(b"crop-A")                     # back to the first frame (a rerun after a captcha)
            third = S.cached_search(q, cache)
            fewer = S.cached_search(q, cache, pages=("sites",))
        self.assertEqual(first["pins"], ["pins-for-crop-A"])
        self.assertEqual(second["pins"], ["pins-for-crop-B"])
        self.assertEqual(third["pins"], ["pins-for-crop-A"])
        self.assertEqual(fewer["pins"], ["pins-for-crop-A"])
        self.assertEqual(calls, ["crop-A", "crop-B"], "identical frames are never searched twice")
        names = sorted(p.name for p in cache.glob("s003_0-*.json"))
        self.assertEqual(len(names), 2, names)
        self.assertTrue(all(len(n) == len("s003_0-") + 16 + len(".json") for n in names), names)
        self.assertEqual(json.loads((cache / names[0]).read_text())["sha256"][:16], names[0][7:23])
        with self.assertRaises(S.SourceFinderError):
            S.cached_search(self.tmp / "missing.jpg", cache)

    def test_rate_limit_waits_between_calls_and_has_a_floor(self):
        waits = []
        with mock.patch.object(S.time, "sleep", waits.append), mock.patch.object(S.time, "monotonic", return_value=1000.0):
            S._LAST_CALL[0] = 999.0
            S._throttle(5)
            S._LAST_CALL[0] = 999.0
            S._throttle(0.1)
        self.assertAlmostEqual(waits[0], 4.0)
        self.assertAlmostEqual(waits[1], S.MIN_DELAY - 1.0)

    def test_inputs(self):
        self.assertEqual(S.check_crop("crop=iw:ih*0.6:0:ih*0.2"), "crop=iw:ih*0.6:0:ih*0.2")
        self.assertEqual(S.check_crop("iw:ih/2:0:0"), "crop=iw:ih/2:0:0")
        for bad in ("crop=iw:ih:0:0,movie=/etc/passwd", "scale=10:10", "crop=iw:ih;drawtext=text=x"):
            with self.assertRaises(S.SourceFinderError):
                S.check_crop(bad)
        self.assertEqual(S.shot_times(2.0, 4.0, 3), [2.35, 3.0, 3.65])
        self.assertEqual(S.shot_times(0.0, 0.4, 3), [0.1, 0.2, 0.3])
        self.assertEqual(S.shot_times(1.0, 2.0, 1), [1.5])
        self.assertEqual(S.parse_shots("0,3-5"), {0, 3, 4, 5})
        self.assertEqual([(s["start"], s["end"]) for s in S.load_cuts("0,1.5,4")], [(0.0, 1.5), (1.5, 4.0)])
        with self.assertRaises(S.SourceFinderError):
            S.load_cuts("0,2,1")

    def test_candidates_from_pin_ids_urls_and_search_json(self):
        js = self.tmp / "search.json"
        js.write_text(json.dumps([{"pins": ["111111111", "222222222"]}]))
        got = []

        def fake_dl(pid, cand_dir, timeout=120):
            got.append(pid)
            f = Path(cand_dir) / f"p{pid}.mp4"
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_bytes(b"v")
            return f

        with mock.patch.object(S, "download_pin", fake_dl), mock.patch.object(S, "_curl", no_network):
            c = S.resolve_candidates(["333333333,https://www.pinterest.com/pin/title--444444444/", str(js), "111111111"],
                                     self.tmp, max_pins=3)
        self.assertEqual(sorted(got), ["111111111", "333333333", "444444444"])
        self.assertEqual({x["url"] for x in c}, {S.pin_url(p) for p in got})
        offline = S.resolve_candidates(["999999999"], self.tmp, download=False)
        self.assertEqual(offline, [])
        with self.assertRaises(S.SourceFinderError):
            S.resolve_candidates(["not-a-pin"], self.tmp, download=False)


@unittest.skipUnless(HAVE_CV, "OpenCV/numpy not installed")
class MatchAndCuts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp())
        cls.m = S.Matcher()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_warped_noisy_copy_scores_far_above_unrelated(self):
        a = scene(1)
        same = self.m.score_images(a, warp(a))
        bigger = self.m.score_images(a, cv2.resize(warp(a, seed=3), (1280, 720)))
        unrelated = max(self.m.score_images(a, scene(s)) for s in (2, 3, 99))
        self.assertGreaterEqual(same, S.EXACT, same)
        self.assertGreaterEqual(bigger, S.EXACT, bigger)
        self.assertLess(unrelated, S.POSSIBLE, unrelated)
        self.assertGreater(same, 20 * max(unrelated, 1))
        self.assertEqual(S.verdict(same), "exact")
        self.assertEqual(S.verdict(unrelated), "none")

    def test_match_finds_the_clip_and_the_moment(self):
        d = self.tmp / "cands"
        d.mkdir()
        target = scene(1)
        write_video(d / "source.avi", moving(scene(5), 20) + [warp(target)] * 10 + moving(scene(6), 10))
        write_video(d / "other.avi", moving(scene(7), 20) + moving(scene(8), 20))
        cv2.imwrite(str(d / "still.jpg"), scene(9))
        (d / "notes.txt").write_text("ignored")
        q = self.tmp / "query.jpg"
        cv2.imwrite(str(q), target)
        res = S.match_candidates([q], S.resolve_candidates([d], self.tmp, download=False), self.m)
        self.assertEqual([r["candidate"] for r in res][0], "source.avi")
        self.assertEqual(len(res), 3)
        best = res[0]
        self.assertEqual(best["verdict"], "exact")
        self.assertIn(best["t"], (2.0, 2.5))
        self.assertTrue(all(r["verdict"] == "none" for r in res[1:]), res)
        still = [r for r in res if r["candidate"] == "still.jpg"][0]
        self.assertIsNone(still["t"])
        self.assertTrue(all("error" not in r for r in res), res)

    def test_an_undecodable_candidate_is_reported_and_the_rest_still_match(self):
        d = self.tmp / "cands_broken"
        d.mkdir()
        target = scene(1)
        write_video(d / "good.avi", moving(scene(5), 10) + [warp(target)] * 10)
        (d / "broken.jpg").write_bytes(b"not really a jpeg")
        (d / "broken.mp4").write_bytes(b"not really a video")
        q = self.tmp / "query_broken.jpg"
        cv2.imwrite(str(q), target)
        res = S.match_candidates([q], S.resolve_candidates([d], self.tmp, download=False), self.m)
        self.assertEqual(res[0]["candidate"], "good.avi")
        self.assertEqual(res[0]["verdict"], "exact")
        bad = {r["candidate"]: r for r in res[1:]}
        self.assertEqual(set(bad), {"broken.jpg", "broken.mp4"})
        for r in bad.values():
            self.assertEqual((r["score"], r["verdict"], r["frames_checked"]), (0, "none", 0), r)
        self.assertIn("cannot read image", bad["broken.jpg"]["error"])
        self.assertIn("no frame could be decoded", bad["broken.mp4"]["error"])
        out = self.tmp / "match_broken.json"
        r = subprocess.run([sys.executable, str(SCRIPT), "match", str(q), "--candidates", str(d), "--work",
                            str(self.tmp / "w_broken"), "--out", str(out)], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("skipped candidate broken.jpg", r.stderr)
        self.assertEqual(json.loads(out.read_text())["results"][0]["candidate"], "good.avi")
        # an unreadable query frame is still an error for the whole call
        bad_q = self.tmp / "bad_query.jpg"
        bad_q.write_bytes(b"nope")
        with self.assertRaises(S.SourceFinderError):
            S.match_candidates([bad_q], S.resolve_candidates([d], self.tmp, download=False), self.m)

    def test_cuts_on_a_synthetic_video(self):
        v = write_video(self.tmp / "three.avi", moving(scene(11), 12) + moving(scene(12), 15) + moving(scene(13), 10))
        c = S.detect_cuts(v, keep_scores=True)
        self.assertEqual(c["cut_frames"], [12, 27])
        self.assertEqual(c["boundaries"], [0.0, 1.2, 2.7, 3.7])
        self.assertEqual(len(c["shots"]), 3)
        in_shot = [s for i, s in enumerate(c["scores"], start=1) if i not in (12, 27)]
        self.assertLess(max(in_shot), 27)
        out = self.tmp / "cuts.json"
        r = subprocess.run([sys.executable, str(SCRIPT), "cuts", str(v), "--out", str(out)], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(out.read_text())["boundaries"], [0.0, 1.2, 2.7, 3.7])


@unittest.skipUnless(HAVE_CV and HAVE_FF, "OpenCV/numpy or ffmpeg not installed")
class FramesAndRunChain(unittest.TestCase):
    CROP = "crop=iw:ih*0.8:0:ih*0.1"

    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp())
        cls.ref = write_video(cls.tmp / "reference.avi",
                              moving(scene(11), 12) + moving(scene(12), 15) + moving(scene(13), 10))
        cls.cands = cls.tmp / "cands"
        cls.cands.mkdir()
        write_video(cls.cands / "p123456789.avi", moving(scene(30), 10) + [warp(scene(12))] * 10)
        write_video(cls.cands / "unrelated.avi", moving(scene(31), 20))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_frames_are_cropped_per_shot(self):
        out = self.tmp / "q"
        m = S.extract_frames(self.ref, S.load_cuts("0,1.2,2.7,3.7"), out, self.CROP, per_shot=2, full=True)
        self.assertEqual(len(m["shots"]), 3)
        q = cv2.imread(m["shots"][1]["queries"][0]["path"])
        full = cv2.imread(m["shots"][1]["full"]["path"])
        self.assertEqual(q.shape[:2], (288, 640))
        self.assertEqual(full.shape[:2], (360, 640))
        self.assertTrue((out / "frames.json").is_file())

    def test_run_offline_against_a_folder(self):
        work = self.tmp / "work_folder"
        r = subprocess.run([sys.executable, str(SCRIPT), "run", str(self.ref), "--work", str(work), "--crop", self.CROP,
                            "--candidates", str(self.cands)], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        rep = json.loads((work / "report.json").read_text())
        self.assertEqual([s["verdict"] for s in rep["shots"]], ["none", "exact", "none"])
        self.assertEqual(rep["shots"][1]["best"]["candidate"], "pin:123456789")
        self.assertEqual(rep["shots"][1]["best"]["url"], "https://www.pinterest.com/pin/123456789/")
        self.assertEqual(rep["summary"], {"shots": 3, "searched": 3, "exact": 1, "possible": 0, "none": 2})
        self.assertEqual(rep["ranked"][0]["shot"], 1)
        self.assertIn("credit", rep["credit"].lower())

    def test_run_offline_survives_a_corrupt_image_in_the_candidates_folder(self):
        cands = self.tmp / "cands_with_junk"
        shutil.copytree(self.cands, cands)
        (cands / "broken.jpg").write_bytes(b"not really a jpeg")
        work = self.tmp / "work_junk"
        r = subprocess.run([sys.executable, str(SCRIPT), "run", str(self.ref), "--work", str(work), "--crop", self.CROP,
                            "--candidates", str(cands)], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        rep = json.loads((work / "report.json").read_text())
        self.assertEqual([s["verdict"] for s in rep["shots"]], ["none", "exact", "none"])
        self.assertEqual(rep["summary"]["searched"], 3)
        junk = [t for t in rep["shots"][1]["top"] if t["candidate"] == "broken.jpg"]
        self.assertEqual(len(junk), 1)
        self.assertIn("cannot read image", junk[0]["error"])

    def test_run_search_path_with_fakes_and_captcha_stop(self):
        work = self.tmp / "work_search"
        calls = []

        def fake_search(image, pages=S.PAGES, delay=4.0):
            calls.append(Path(image).name)
            if Path(image).name.startswith("s002"):
                raise S.CaptchaError("fake captcha")
            pins = ["123456789", "888888888"] if Path(image).name.startswith("s001") else []
            return {"image": str(image), "cbir_id": "x", "pages": {p: {} for p in pages}, "pins": pins,
                    "pinterest": [S.pin_url(p) for p in pins], "leads": []}

        def fake_dl(pid, cand_dir, timeout=120):
            src = self.cands / f"p{pid}.avi"
            if not src.is_file():
                return None
            dst = Path(cand_dir) / f"p{pid}.mp4"
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
            return dst

        with mock.patch.object(S, "yandex_search", fake_search), mock.patch.object(S, "download_pin", fake_dl), \
                mock.patch.object(S, "_curl", no_network):
            rep = S.run(self.ref, work, crop=self.CROP)
        self.assertEqual(rep["shots"][0]["verdict"], "none")
        self.assertEqual(rep["shots"][1]["verdict"], "exact")
        self.assertEqual(rep["shots"][1]["pins_found"], 2)
        self.assertEqual(rep["shots"][1]["candidates"], 1)
        self.assertTrue(rep["stopped"].startswith("captcha at shot 2"), rep["stopped"])
        self.assertFalse(rep["shots"][2]["searched"])
        self.assertEqual(rep["summary"]["searched"], 2)
        self.assertEqual(calls.count("s002_0.jpg"), 1)
        self.assertNotIn("s002_1.jpg", calls)
        self.assertEqual(len(list((work / "search").glob("s001_full-*.json"))), 1)
        with mock.patch.object(S, "yandex_search", no_network), mock.patch.object(S, "download_pin", fake_dl):
            again = S.cached_search(work / "queries" / "s001_0.jpg", work / "search")
        self.assertEqual(again["pins"], ["123456789", "888888888"])


if __name__ == "__main__":
    unittest.main()
