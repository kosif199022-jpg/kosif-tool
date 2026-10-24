"""Offline tests for scripts/instagram_finder.py (no Instagram traffic: yt-dlp is faked)."""
from __future__ import annotations

import io
import json
import os
import shutil
import stat
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL / "scripts"))
import instagram_finder as ig  # noqa: E402

FAKE_YTDLP = r'''#!/usr/bin/env python3
import json, sys
argv = sys.argv[1:]
if "--list-impersonate-targets" in argv or "--version" in argv:
    sys.exit(0)
url = argv[-1]
sc = url.rstrip("/").rsplit("/", 1)[-1]
if "--dump-json" in argv:
    print(json.dumps({"id": sc, "channel": "suki.shotz", "description": "Perfume splash in slow motion #perfume #productvideo",
                      "duration": 12.0, "view_count": 5000, "upload_date": "20261001", "thumbnail": "https://cdn.example/t.jpg"}))
    sys.exit(0)
tpl = argv[argv.index("-o") + 1]
path = tpl.replace("%(title).120B", "clip").replace("%(id)s", sc).replace("%(ext)s", "mp4")
open(path, "wb").write(b"fake")
print(path)
'''

LINKS = [
    "https://www.instagram.com/mcydro?cplk=bzk1MTlyYjBldm9q",
    "https://www.instagram.com/ayman_mamdouh_ph?xtok=dmd3bHZqNzA2bjVl",
    "https://www.instagram.com/suki.shotz?dlrf=MTNwY3hhZjZ6cW54Mw==",
    "https://www.instagram.com/asirgokerr?obrf=bmVrOTZrbGx2cmhu",
    "https://www.instagram.com/brkn.land?rpxt=MThuNXBxNzhqNTlqMQ==",
]


def run(*argv) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        try:
            rc = ig.main(list(argv))
        except SystemExit as e:  # argparse
            rc = e.code
    return rc, out.getvalue(), err.getvalue()


class Accounts(unittest.TestCase):
    def test_owner_links_are_saved_clean(self):
        saved = {a["handle"]: a["url"] for a in ig.load_sources()["accounts"]}
        for link in LINKS:
            acc = ig.normalize_account(link)
            self.assertNotIn("?", acc["url"])
            self.assertEqual(saved.get(acc["handle"]), acc["url"])
        self.assertEqual(len(saved), 5)

    def test_rejects_non_instagram_and_reserved(self):
        for bad in ("https://evil.example/mcydro", "https://www.instagram.com/explore/", "https://www.instagram.com/"):
            with self.assertRaises(ValueError):
                ig.normalize_account(bad)
        self.assertEqual(ig.normalize_account("@Brkn.Land")["handle"], "brkn.land")

    def test_add_and_remove_account_on_copy(self):
        with tempfile.TemporaryDirectory() as d:
            src = Path(d) / "s.json"
            shutil.copy(ig.SOURCES, src)
            rc, out, _ = run("--sources", str(src), "add-account", "https://instagram.com/new.one/?igsh=abc", LINKS[0])
            self.assertEqual(rc, 0)
            self.assertIn("saved @new.one", out)
            self.assertIn("already saved: @mcydro", out)
            run("--sources", str(src), "remove-account", "@new.one")
            self.assertEqual(len(json.loads(src.read_text())["accounts"]), 5)

    def test_post_url_cleaning(self):
        self.assertEqual(ig.clean_post_url("https://www.instagram.com/reels/AbC_12-x/?igsh=1"),
                         "https://www.instagram.com/reel/AbC_12-x/")
        self.assertEqual(ig.clean_post_url("https://instagram.com/suki.shotz/p/XyZ123/"), "https://www.instagram.com/p/XyZ123/")
        self.assertIsNone(ig.clean_post_url("https://www.instagram.com/suki.shotz/"))


class Search(unittest.TestCase):
    IDX = {"posts": {
        "A1": ig.post_record(shortcode="A1", account="suki.shotz", is_video=True, caption="عطر رجالي فخم 🔥 تصوير منتجات",
                             hashtags=["perfume", "productphotography"], views=20000, duration=15),
        "B2": ig.post_record(shortcode="B2", account="mcydro", is_video=True, caption="Burger commercial in studio light #foodvideo",
                             duration=30, alt="May be an image of burger"),
        "C3": ig.post_record(shortcode="C3", account="brkn.land", is_video=False, caption="Perfume bottle still #perfume"),
        "D4": ig.post_record(shortcode="D4", account="asirgokerr", is_video=True, caption="Fragrance splash, slow motion",
                             duration=8),
    }}

    def test_arabic_query_finds_english_tagged_video(self):
        hits = ig.search(self.IDX, "برفان")
        self.assertEqual([h["shortcode"] for h in hits][:2], ["A1", "D4"])
        self.assertNotIn("C3", [h["shortcode"] for h in hits])  # photos excluded by default

    def test_normalisation_and_filters(self):
        self.assertEqual(ig.norm_text("العِطْرُ"), "العطر")
        self.assertEqual(ig.tokens("قهوة"), ig.tokens("قهوه"))
        self.assertEqual([h["shortcode"] for h in ig.search(self.IDX, "perfume", max_dur=10)], ["D4"])
        self.assertIn("C3", [h["shortcode"] for h in ig.search(self.IDX, "perfume", include_photos=True)])
        self.assertEqual([h["shortcode"] for h in ig.search(self.IDX, "برجر")], ["B2"])

    def test_plan_is_offline_and_has_hashtags(self):
        rc, out, _ = run("plan", "عطر رجالي")
        self.assertEqual(rc, 0)
        plan = json.loads(out)
        self.assertIn("perfume", plan["hashtags"])
        self.assertEqual(len(plan["saved_accounts"]), 5)


@unittest.skipIf(os.name == "nt", "fake yt-dlp is a POSIX script")
class Pipeline(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = Path(self.tmp.name)
        fake = self.d / "yt-dlp"
        fake.write_text(FAKE_YTDLP.replace("#!/usr/bin/env python3", "#!" + sys.executable))
        fake.chmod(fake.stat().st_mode | stat.S_IEXEC)
        self.old = os.environ.get("YTDLP")
        os.environ["YTDLP"] = str(fake)
        self.idx = str(self.d / "index.json")

    def tearDown(self):
        if self.old is None:
            os.environ.pop("YTDLP", None)
        else:
            os.environ["YTDLP"] = self.old
        self.tmp.cleanup()

    def test_add_posts_search_download(self):
        rc, out, err = run("--index", self.idx, "add-posts", "https://www.instagram.com/reel/AAA111/?igsh=x",
                           "https://example.com/nope", "--sleep", "0")
        self.assertEqual(rc, 2, err)  # one bad link skipped
        self.assertIn("@suki.shotz", out)
        hits = str(self.d / "hits.json")
        rc, out, _ = run("--index", self.idx, "search", "عطر", "--save", hits)
        self.assertEqual(rc, 0)
        self.assertIn("AAA111", out)
        rc, _, err = run("download", hits, "--pick", "1", "--rights", "permission")
        self.assertEqual(rc, 2)
        self.assertIn("--evidence", err)
        rc, out, _ = run("download", hits, "--pick", "1", "--rights", "owned", "--dry-run", "-o", str(self.d / "v"),
                         "--cookies-from-browser", "firefox")
        self.assertEqual(rc, 0)
        self.assertIn("fetch_video.py", out)
        self.assertIn("--cookies-from-browser", out)
        rc, out, err = run("download", hits, "--pick", "1", "--rights", "permission", "--evidence", "DM 2026-10-24",
                           "--no-safe", "--sleep", "0", "-o", str(self.d / "v"), "--cookies-from-browser", "firefox")
        self.assertEqual(rc, 0, err)
        log = [json.loads(l) for l in (self.d / "v" / "instagram_rights.jsonl").read_text().splitlines()]
        self.assertEqual(log[0]["credit"], "@suki.shotz")
        self.assertTrue(Path(log[0]["file"]).is_file())

    def test_download_cap(self):
        hits = self.d / "h.json"
        hits.write_text(json.dumps({"hits": [{"rank": i, "url": f"https://www.instagram.com/reel/X{i}abc/", "shortcode": f"X{i}"}
                                             for i in range(1, 40)]}))
        rc, _, err = run("download", str(hits), "--top", "30", "--rights", "owned", "--dry-run")
        self.assertEqual(rc, 2)
        self.assertIn("cap", err)


if __name__ == "__main__":
    unittest.main()
