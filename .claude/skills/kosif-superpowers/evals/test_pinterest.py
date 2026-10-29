"""Offline tests for the shared Pinterest pin helper (_pinterest.py) and its two users, fetch_video.py and
source_finder.py. No network: every yt-dlp answer comes from evals/fixtures/pinterest/<class>.json (shaped
like `yt-dlp -J` output and stderr, synthetic ids and URLs), played back by a fake yt-dlp program that logs
each call; the media files are synthetic clips made with ffmpeg (those tests skip without ffmpeg/ffprobe)."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parent / "scripts"
FIX = HERE / "fixtures" / "pinterest"
sys.path.insert(0, str(SCRIPTS))
import _pinterest as P  # noqa: E402
import fetch_video as FV  # noqa: E402
import source_finder as S  # noqa: E402

HAVE_FF = bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))
VIDEO_ID = "100000000000000001"

FAKE = r'''#!PYTHON
"""Fake yt-dlp: plays back evals/fixtures/pinterest/*.json; logs every call to $FAKE_PIN_LOG."""
import json, os, re, shutil, sys
from pathlib import Path
args = sys.argv[1:]
fx_dir, pins = Path(os.environ["FAKE_PIN_DIR"]), json.loads(os.environ["FAKE_PIN_MAP"])
def load(name):
    return json.loads((fx_dir / name).read_text(encoding="utf-8"))
def log(**kw):
    with open(os.environ["FAKE_PIN_LOG"], "a", encoding="utf-8") as f:
        f.write(json.dumps(dict(kw, args=args)) + "\n")
if "-J" in args:
    pid = re.search(r"/pin/(\d+)", args[args.index("--") + 1]).group(1)
    log(op="probe", pin=pid)
    fx = load(pins[pid])
    p = fx["probe"]
    out = load(p["stdout_from"])["probe"]["stdout"] if "stdout_from" in p else p.get("stdout")
    text = json.dumps(out)
    if isinstance(out, dict) and out.get("extractor_key") == "Pinterest":
        text = text.replace(out["id"], pid)
    sys.stdout.write(text + "\n")
    sys.stderr.write(p.get("stderr", ""))
    sys.exit(p.get("returncode", 0))
if "--load-info-json" in args:
    info = json.loads(Path(args[args.index("--load-info-json") + 1]).read_text(encoding="utf-8"))
    pid = info["id"]
    dl = load(pins[pid]).get("download", {})
    tmpl = Path(args[args.index("-o") + 1])
    out_dir, stem = tmpl.parent, tmpl.name.split(".%(ext)s")[0]
    log(op="download", pin=pid, out_dir=str(out_dir))
    for frag in ("fV_HLSV3_MOBILE-1839.mp4", "fV_HLSV3_MOBILE-audio1-1.mp4"):   # left behind on purpose
        (out_dir / f"{stem}.{frag}").write_bytes(b"\0" * 64)
    if dl.get("returncode", 0):
        sys.stderr.write(dl.get("stderr", ""))
        sys.exit(dl["returncode"])
    ext = dl.get("writes", "mp4")
    dst = out_dir / f"{stem}.{ext}"
    shutil.copyfile(os.environ["FAKE_PIN_GIF" if ext == "gif" else "FAKE_PIN_MP4"], dst)
    print(dst)
    sys.exit(0)
sys.stderr.write("fake yt-dlp: unexpected call " + " ".join(args) + "\n")
sys.exit(2)
'''


def fixture(name):
    return json.loads((FIX / name).read_text(encoding="utf-8"))


def probe_stdout(fx):
    p = fx["probe"]
    return fixture(p["stdout_from"])["probe"]["stdout"] if "stdout_from" in p else p.get("stdout")


class ClassifyFixtures(unittest.TestCase):
    """Pure classification of every fixture class; no programs are run."""

    def test_every_fixture_class_is_classified_at_probe_and_download(self):
        names = sorted(p.name for p in FIX.glob("*.json"))
        self.assertGreaterEqual(len(names), 11)
        seen = set()
        for name in names:
            fx = fixture(name)
            out = probe_stdout(fx)
            v = P.classify_info(out) if fx["probe"].get("returncode", 0) == 0 else P.classify_error(fx["probe"]["stderr"])
            self.assertEqual(v["kind"], fx["expect"]["probe"], name)
            self.assertTrue(v["reason"] and "\n" not in v["reason"], name)
            if fx.get("download", {}).get("returncode"):
                d = P.classify_error(fx["download"]["stderr"], "download")
                self.assertEqual(d["kind"], fx["expect"]["final"], name)
            if "embed_url" in fx["expect"]:
                self.assertEqual(v.get("embed_url"), fx["expect"]["embed_url"], name)
            seen.add(fx["expect"]["final"])
        self.assertTrue({"video", "image", "gif", "youtube", "embedded", "deleted", "cdn-refused", "blocked"} <= seen)

    def test_video_label_is_the_display_size(self):
        v = P.classify_info(probe_stdout(fixture("video.json")))
        self.assertEqual((v["label_size"], v["label_format"]), ("1080x1920", "V_720P"))
        self.assertIsNone(v["retry"])

    def test_embedded_youtube_is_named_and_never_retried(self):
        for name in ("youtube.json", "youtube_botcheck.json", "youtube_resolved.json"):
            fx = fixture(name)
            out = probe_stdout(fx)
            v = P.classify_info(out) if fx["probe"]["returncode"] == 0 else P.classify_error(fx["probe"]["stderr"])
            self.assertTrue(v["reason"].startswith("embedded YouTube, blocked on cloud"), name)
            self.assertEqual((v["permanent"], v["retry"]), (True, "never"), name)
            self.assertIn("not bypassed", v["reason"])

    def test_deleted_and_cdn_refused_are_told_apart(self):
        deleted = P.classify_error(fixture("deleted.json")["probe"]["stderr"], "probe")
        refused = P.classify_error(fixture("cdn_refused.json")["download"]["stderr"], "download")
        blocked = P.classify_error(fixture("blocked.json")["probe"]["stderr"], "probe")
        self.assertEqual((deleted["kind"], deleted["permanent"], deleted["retry"]), ("deleted", True, "never"))
        self.assertEqual((refused["kind"], refused["permanent"], refused["retry"]), ("cdn-refused", False, "not in this run"))
        self.assertEqual((blocked["kind"], blocked["permanent"]), ("blocked", False))
        self.assertIn("HTTP 404", deleted["reason"])
        self.assertIn("HTTP 403", refused["reason"])
        meta403 = P.classify_error("ERROR: [Pinterest] 1: Unable to download JSON metadata: HTTP Error 403: Forbidden")
        self.assertEqual(meta403["kind"], "blocked")
        self.assertEqual(P.classify_error("ERROR: [Pinterest] 1: No video formats found!")["kind"], "image")
        old = P.classify_error("yt-dlp: error: no such option: --use-extractors")
        self.assertIn("--update", old["reason"])
        self.assertEqual(P.classify_error("ERROR: something new broke")["kind"], "error")

    def test_links(self):
        self.assertEqual(P.pin_id("https://www.pinterest.co.uk/pin/some-title--123456789/"), "123456789")
        self.assertEqual(P.pin_id(" 6403624444785202 "), "6403624444785202")
        self.assertIsNone(P.pin_id("12345"))
        self.assertTrue(P.is_pin_link("https://www.pinterest.com/pin/782359766544232782/"))
        self.assertTrue(P.is_pin_link("https://pin.it/AbCdEf123"))
        self.assertFalse(P.is_pin_link("https://www.pinterest.com/someone/quran-boards/"))
        self.assertFalse(P.is_pin_link("https://example.com/?u=pinterest.com/pin/123456789"))
        self.assertIs(S.PIN_RE, P.PIN_RE)
        self.assertEqual(S.pin_url("123456789"), "https://www.pinterest.com/pin/123456789/")

    def test_short_link_is_followed_once(self):
        class R:
            def __init__(self, url):
                self.url = url

            def geturl(self):
                return self.url

            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

        with mock.patch.object(P, "_open", return_value=R("https://www.pinterest.com/pin/123456789/sent/?invite_code=x")) as op:
            rec, url = P._start("https://pin.it/AbCdEf123")
        self.assertEqual(op.call_count, 1)
        self.assertEqual((url, rec["pin_id"], rec.get("kind")), ("https://www.pinterest.com/pin/123456789/", "123456789", None))
        with mock.patch.object(P, "_open", side_effect=OSError("offline")):
            rec, _url = P._start("https://pin.it/AbCdEf123")
        self.assertEqual(rec["kind"], "error")
        self.assertIn("pin.it", rec["reason"])

    def test_credit_record(self):
        c = P.credit_record("https://www.pinterest.com/pin/1/", probe_stdout(fixture("video.json")))
        self.assertEqual((c["uploader"], c["licence"]), ("Example Creator", "licence unknown — credit and link"))
        self.assertIn("by Example Creator", c["line"])
        bare = P.credit_record("https://www.pinterest.com/pin/1/", None)
        self.assertIsNone(bare["uploader"])
        self.assertIn("uploader unknown", bare["line"])

    def test_still_kind_by_extension_then_codec(self):
        self.assertEqual(P.still_kind("p1.gif", {}), "gif")
        self.assertEqual(P.still_kind("p1.mp4", {"vcodec": "gif"}), "gif")
        self.assertEqual(P.still_kind("p1.jpg", {"vcodec": "mjpeg"}), "image")
        self.assertEqual(P.still_kind("p1.webp", {}), "image")
        self.assertIsNone(P.still_kind("p1.mp4", {"vcodec": "h264"}))
        self.assertIsNone(P.still_kind("p1.mov", {"vcodec": "mjpeg"}))      # Motion JPEG video stays video


@unittest.skipUnless(HAVE_FF, "ffmpeg/ffprobe not installed")
class FetchWithFakeYtdlp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.media = Path(tempfile.mkdtemp(prefix="pin_media_"))
        cls.mp4 = cls.media / "v720.mp4"
        cls.gif = cls.media / "anim.gif"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc=size=720x1280:rate=30:duration=1",
                        "-f", "lavfi", "-i", "sine=frequency=440:duration=1", "-c:v", "mpeg4", "-q:v", "6",
                        "-c:a", "aac", "-shortest", str(cls.mp4)], check=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc=size=250x250:rate=5:duration=1",
                        str(cls.gif)], check=True)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.media, ignore_errors=True)

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="pin_test_"))
        self.out = self.tmp / "out"
        self.log = self.tmp / "calls.jsonl"
        fake = self.tmp / "yt-dlp"
        fake.write_text(FAKE.replace("#!PYTHON", "#!" + sys.executable), encoding="utf-8")
        fake.chmod(0o755)
        self.map = {VIDEO_ID: "video.json", "100000000000000002": "image.json", "100000000000000003": "gif_embed.json",
                    "100000000000000004": "gif_format.json", "100000000000000005": "gif_file.json",
                    "100000000000000006": "youtube.json", "100000000000000007": "deleted.json",
                    "100000000000000008": "cdn_refused.json", "100000000000000009": "blocked.json",
                    "100000000000000010": "vimeo.json"}
        for k in range(11, 16):
            self.map[f"1000000000000000{k}"] = "video.json"
        self.env = mock.patch.dict(os.environ, {"YTDLP": str(fake), "FAKE_PIN_DIR": str(FIX), "FAKE_PIN_LOG": str(self.log),
                                                "FAKE_PIN_MAP": json.dumps(self.map), "FAKE_PIN_MP4": str(self.mp4),
                                                "FAKE_PIN_GIF": str(self.gif)})
        self.env.start()
        self.ytdlp = [str(fake)]
        P.reset_memory()

    def tearDown(self):
        self.env.stop()
        P.reset_memory()
        shutil.rmtree(self.tmp, ignore_errors=True)

    def calls(self, op=None, pin=None):
        if not self.log.is_file():
            return []
        rows = [json.loads(line) for line in self.log.read_text(encoding="utf-8").splitlines()]
        return [r for r in rows if (op is None or r["op"] == op) and (pin is None or r["pin"] == pin)]

    def listing(self, d=None):
        d = Path(d or self.out)
        return sorted(p.relative_to(d).as_posix() for p in d.rglob("*")) if d.is_dir() else []

    def test_video_pin_is_measured_moved_and_credited(self):
        rec = P.fetch(VIDEO_ID, self.out, ytdlp=self.ytdlp)
        self.assertEqual(rec["kind"], "video", rec)
        self.assertEqual(rec["file"], str(self.out / f"p{VIDEO_ID}.mp4"))
        self.assertEqual((rec["width"], rec["height"]), (720, 1280))           # ffprobe, not the 1080x1920 label
        self.assertEqual(rec["label_size"], "1080x1920")
        self.assertTrue(rec["resolution_verified"])
        self.assertIn("1080x1920", rec["size_note"])
        self.assertIn("720x1280", rec["size_note"])
        self.assertTrue(rec["audio"].startswith("kept"))
        self.assertEqual(self.listing(), [f"p{VIDEO_ID}.mp4", f"p{VIDEO_ID}.pin.json"])   # no fragments, no temp dir
        side = json.loads((self.out / f"p{VIDEO_ID}.pin.json").read_text(encoding="utf-8"))
        self.assertEqual(side["schema"], P.SCHEMA)
        self.assertEqual(side["credit"]["licence"], "licence unknown — credit and link")
        self.assertEqual(side["credit"]["pin"], P.pin_url(VIDEO_ID))
        probe_call = self.calls("probe")[0]["args"]
        self.assertIn("-J", probe_call)
        self.assertEqual(probe_call[probe_call.index("--use-extractors") + 1], "pinterest")
        dl = self.calls("download")[0]
        self.assertNotEqual(Path(dl["out_dir"]), self.out)                       # downloaded in a temp folder
        self.assertEqual(Path(dl["out_dir"]).parent, self.out)
        self.assertFalse(Path(dl["out_dir"]).exists())                           # ... removed afterwards

    def test_strip_audio_drops_the_pins_music(self):
        rec = P.fetch(VIDEO_ID, self.out, ytdlp=self.ytdlp, strip_audio=True)
        self.assertEqual(rec["audio"], "stripped")
        self.assertIsNone(rec["acodec"])
        self.assertIsNone(P.probe_media(rec["file"])["acodec"])
        self.assertEqual(P.probe_media(rec["file"])["vcodec"], "mpeg4")         # video copied, not re-encoded

    def test_non_video_pins_are_never_downloaded_or_retried(self):
        for pid, kind in (("100000000000000002", "image"), ("100000000000000003", "gif"), ("100000000000000004", "gif"),
                          ("100000000000000006", "youtube"), ("100000000000000007", "deleted"),
                          ("100000000000000010", "embedded")):
            rec = P.fetch(pid, self.out, ytdlp=self.ytdlp)
            self.assertEqual((rec["kind"], rec["file"]), (kind, None), pid)
            self.assertTrue(rec["permanent"])
            P.fetch(pid, self.out, ytdlp=self.ytdlp)                             # same run: remembered
            P.reset_memory()
            again = P.fetch(pid, self.out, ytdlp=self.ytdlp)                     # a later run: the sidecar says never
            self.assertTrue(again["cached"])
            self.assertEqual(len(self.calls("probe", pid)), 1, pid)
            self.assertEqual(self.calls("download", pid), [], pid)
        yt = P.read_record(self.out, "p100000000000000006")
        self.assertTrue(yt["reason"].startswith("embedded YouTube, blocked on cloud"))
        self.assertEqual(yt["embed_url"], "https://www.youtube.com/watch?v=AAAAAAAAAAA")
        self.assertEqual([p for p in self.listing() if not p.endswith(".pin.json")], [])

    def test_cdn_refused_is_tried_once_per_run_and_leaves_nothing(self):
        pid = "100000000000000008"
        rec = P.fetch(pid, self.out, ytdlp=self.ytdlp)
        self.assertEqual((rec["kind"], rec["file"], rec["retry"]), ("cdn-refused", None, "not in this run"))
        self.assertTrue(P.fetch(pid, self.out, ytdlp=self.ytdlp)["repeated"])
        self.assertEqual((len(self.calls("probe", pid)), len(self.calls("download", pid))), (1, 1))
        self.assertEqual(self.listing(), [f"p{pid}.pin.json"])                  # the fragment went with the temp dir
        P.reset_memory()                                                         # a later run may try once more
        P.fetch(pid, self.out, ytdlp=self.ytdlp)
        self.assertEqual((len(self.calls("probe", pid)), len(self.calls("download", pid))), (2, 2))
        self.assertEqual(P.fetch(pid, self.out, ytdlp=self.ytdlp)["kind"], "cdn-refused")
        blocked = P.fetch("100000000000000009", self.out, ytdlp=self.ytdlp)
        self.assertEqual((blocked["kind"], blocked["permanent"]), ("blocked", False))

    def test_a_gif_that_arrives_as_the_file_is_treated_as_an_image(self):
        rec = P.fetch("100000000000000005", self.out, ytdlp=self.ytdlp)
        self.assertEqual((rec["kind"], rec["file"]), ("gif", None))
        self.assertIn("250x250", rec["reason"])
        self.assertEqual(self.listing(), ["p100000000000000005.pin.json"])

    def test_a_finished_file_is_reused_and_stripped_later(self):
        P.fetch(VIDEO_ID, self.out, ytdlp=self.ytdlp)
        P.reset_memory()
        rec = P.fetch(VIDEO_ID, self.out, ytdlp=self.ytdlp, strip_audio=True)
        self.assertTrue(rec["reused"])
        self.assertEqual(rec["audio"], "stripped")
        self.assertIsNone(P.probe_media(rec["file"])["acodec"])
        self.assertEqual(len(self.calls("download", VIDEO_ID)), 1)

    def test_audio_that_cannot_be_stripped_is_never_kept(self):
        no_ffmpeg = mock.patch.object(P, "remove_audio", return_value=(False, "ffmpeg is not installed"))
        with no_ffmpeg:
            rec = P.fetch(VIDEO_ID, self.out, ytdlp=self.ytdlp, strip_audio=True)
        self.assertEqual((rec["kind"], rec["file"]), ("error", None))
        self.assertIn("music cannot leak", rec["reason"])
        self.assertEqual(self.listing(), [f"p{VIDEO_ID}.pin.json"])            # nothing with music left behind
        P.reset_memory()
        P.fetch(VIDEO_ID, self.out, ytdlp=self.ytdlp)                            # a later run keeps the audio on purpose
        P.reset_memory()
        with no_ffmpeg:
            again = P.fetch(VIDEO_ID, self.out, ytdlp=self.ytdlp, strip_audio=True)
        self.assertEqual((again["kind"], again["file"]), ("error", None))       # reused file is not handed out
        self.assertTrue((self.out / f"p{VIDEO_ID}.mp4").is_file())              # ... and not deleted either

    def test_source_finder_parallel_pins_leave_no_fragments_and_strip_audio(self):
        pins = [f"1000000000000000{k}" for k in range(11, 16)] + ["100000000000000002", "100000000000000006"]
        work = self.tmp / "work"
        oc = {}
        cands = S.resolve_candidates(pins, work, jobs=4, outcomes=oc)
        self.assertEqual(sorted(c["label"] for c in cands), sorted(f"pin:1000000000000000{k}" for k in range(11, 16)))
        cand = work / "cand"
        files = self.listing(cand)
        self.assertEqual(files, sorted([f"p{p}.mp4" for p in pins[:5]] + [f"p{p}.pin.json" for p in pins]))
        self.assertFalse([f for f in files if ".f" in f.split(".", 1)[1]])
        dirs = {c["out_dir"] for c in self.calls("download")}
        self.assertEqual(len(dirs), 5)                                           # one private temp folder per pin
        for c in cands:
            self.assertIsNone(P.probe_media(c["file"])["acodec"])                # source_finder strips by default
        self.assertEqual(oc["counts"], {"image": 1, "video": 5, "youtube": 1})
        self.assertEqual({s["kind"] for s in oc["skipped"]}, {"image", "youtube"})
        kept = S.resolve_candidates(["100000000000000015"], self.tmp / "work2", strip_audio=False)
        self.assertEqual(P.probe_media(kept[0]["file"])["acodec"], "aac")

    def test_fetch_video_cli_routes_pins_through_the_helper(self):
        out = self.tmp / "clips"
        video, image = P.pin_url(VIDEO_ID), "https://www.pinterest.com/pin/example--100000000000000002/"
        with mock.patch("sys.stdout"):
            code = FV.main([video, image, "-o", str(out), "--strip-audio", "--quality", "720"])
        self.assertEqual(code, 1)                                                # the image pin has no video
        man = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
        v, i = man
        self.assertEqual((v["via"], v["kind"], v["audio"], v["width"], v["height"]), ("pinterest", "video", "stripped", 720, 1280))
        self.assertEqual(v["file"], str(out / f"pinterest-{VIDEO_ID}.mp4"))
        self.assertEqual(v["license"], "licence unknown — credit and link")
        self.assertEqual(v["credit"]["uploader"], "Example Creator")
        self.assertEqual((i["kind"], i["file"]), ("image", None))
        self.assertTrue(i["error"].startswith("image pin"))
        self.assertEqual(sorted(p.name for p in out.iterdir()),
                         sorted(["manifest.json", f"pinterest-{VIDEO_ID}.mp4", f"pinterest-{VIDEO_ID}.pin.json",
                                 "pinterest-100000000000000002.pin.json"]))

    def test_fetch_video_youtube_pin_gets_the_blocked_hint(self):
        out = self.tmp / "clips"
        with mock.patch("sys.stdout"):
            FV.main([P.pin_url("100000000000000006"), "-o", str(out)])
        rec = json.loads((out / "manifest.json").read_text(encoding="utf-8"))[0]
        self.assertTrue(rec["blocked"])
        self.assertIn("--cookies-from-browser", rec["hint"])
        self.assertTrue(rec["error"].startswith("embedded YouTube, blocked on cloud"))

    def test_fetch_video_classify_downloads_nothing(self):
        out = self.tmp / "nothing"
        p = subprocess.run([sys.executable, str(SCRIPTS / "fetch_video.py"), "--classify", "-o", str(out),
                            P.pin_url(VIDEO_ID), P.pin_url("100000000000000002"), P.pin_url("100000000000000006"),
                            P.pin_url("100000000000000007")], capture_output=True, text=True, timeout=120)
        self.assertEqual(p.returncode, 0, p.stderr)
        kinds = [line.split()[0] for line in p.stdout.splitlines()]
        self.assertEqual(kinds, ["video", "image", "youtube", "deleted"])
        self.assertFalse(out.exists())
        self.assertEqual(self.calls("download"), [])

    def test_strip_audio_and_audio_quality_conflict(self):
        with mock.patch("sys.stderr"), self.assertRaises(SystemExit):
            FV.main([P.pin_url(VIDEO_ID), "--strip-audio", "--quality", "audio"])


if __name__ == "__main__":
    unittest.main()
