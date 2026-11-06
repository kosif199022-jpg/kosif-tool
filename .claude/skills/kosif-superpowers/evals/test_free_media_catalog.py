"""Free media catalog, offline: the shipped catalog validates, the user's 100-site list is all there with no
duplicates, filters and search links work, and the checker catches the mistakes it exists to catch.

    python3 -m unittest discover -s .claude/skills/kosif-superpowers/evals -p 'test_free_media_catalog.py' -v
"""
import contextlib
import copy
import io
import json
import sys
import unittest
from pathlib import Path
from unittest import mock

SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK / "scripts"))
import free_media_catalog as FMC  # noqa: E402
import free_photos as FP  # noqa: E402

DB = FMC.load()


def run(*argv):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = FMC.main(list(argv))
    return code, buf.getvalue()


class ShippedCatalog(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(FMC.problems(DB, FMC.footage_ids()), [])

    def test_user_list_complete(self):
        user = [s for s in DB["sources"] if s["origin"] == "user-100"]
        self.assertEqual(len(user), 100)
        stars = {s["id"] for s in user if s["star"]}
        self.assertEqual(stars, {"pexels", "pixabay", "mixkit", "coverr", "footagecrate", "nasa-images", "unsplash",
                                 "openverse", "polyhaven"})
        self.assertEqual(DB["counts"]["total"], len(DB["sources"]))

    def test_photo_tool_refs_match_free_photos(self):
        self.assertEqual(set(FMC.PHOTO_SOURCES), set(FP.SOURCES))

    def test_known_licence_facts(self):
        by = {s["id"]: s for s in DB["sources"]}
        for sid in ("pexels", "pixabay", "unsplash", "polyhaven"):
            self.assertEqual((by[sid]["commercial"], by[sid]["credit"]), ("yes", "no"), sid)
        for sid in ("freepik-videos", "vecteezy", "eso", "esahubble", "dareful", "incompetech"):
            self.assertEqual(by[sid]["credit"], "yes", sid)
        for sid in ("british-museum", "bbc-sfx"):
            self.assertEqual(by[sid]["commercial"], "no", sid)
        self.assertEqual(by["wikimedia"]["commercial"], "per-item")

    def test_topics_cover_the_asks(self):
        egypt = {s["id"] for s in FMC.select(DB, topic="egypt")}
        self.assertTrue({"met", "brooklyn", "loc", "nypl", "copernicus"} <= egypt)
        self.assertGreaterEqual(len(FMC.select(DB, topic="nature-4k")), 20)
        self.assertGreaterEqual(len(FMC.select(DB, section="audio")), 10)


class Filters(unittest.TestCase):
    def test_commercial_no_credit(self):
        rows = FMC.select(DB, commercial=True, no_credit=True)
        self.assertTrue(rows)
        self.assertTrue(all(s["commercial"] == "yes" and s["credit"] in ("no", "requested") for s in rows))

    def test_reachable_drops_dead_domains(self):
        dead = [s for s in DB["sources"] if s["reach"] == "no-dns"]
        self.assertEqual(len(FMC.select(DB, reachable=True)), len(DB["sources"]) - len(dead))

    def test_find_all_words(self):
        ids = {s["id"] for s in FMC.find(DB, ["CC0", "museum"])}
        self.assertIn("walters", ids)
        self.assertFalse(FMC.find(DB, ["zzzz-not-a-site"]))

    def test_links_quote_query(self):
        rows = FMC.select(DB, topic="egypt")
        links = dict((s["id"], u) for s, u in FMC.search_links(DB, "pyramids & nile", rows))
        self.assertEqual(links["unsplash"], "https://unsplash.com/s/photos/pyramids%20%26%20nile")
        self.assertNotIn("{q}", "".join(links.values()))


class Checker(unittest.TestCase):
    def broken(self, fn):
        db = copy.deepcopy(DB)
        fn(db)
        return FMC.problems(db, FMC.footage_ids())

    def test_duplicate_url_ignores_www_and_slash(self):
        def dup(db):
            extra = copy.deepcopy(db["sources"][0])
            extra["id"] = "pexels-copy"
            extra["url"] = extra["url"].replace("www.", "").rstrip("/")
            db["sources"].append(extra)
            db["counts"]["total"] += 1
        self.assertTrue(any("same url" in e for e in self.broken(dup)))

    def test_bad_enum_and_tool_ref(self):
        def bad(db):
            db["sources"][0]["commercial"] = "maybe"
            db["sources"][1]["tools"] = ["free_footage:nope"]
        errs = self.broken(bad)
        self.assertTrue(any("commercial" in e for e in errs))
        self.assertTrue(any("free_footage:nope" in e for e in errs))

    def test_http_url_and_search_template(self):
        def bad(db):
            db["sources"][0]["url"] = "http://www.pexels.com/videos/"
            db["sources"][0]["search_url"] = "https://www.pexels.com/search/"
        errs = self.broken(bad)
        self.assertTrue(any("https" in e and "url must" in e for e in errs))
        self.assertTrue(any("search_url" in e for e in errs))


class Cli(unittest.TestCase):
    def test_commands(self):
        code, out = run("check")
        self.assertEqual(code, 0, out)
        code, out = run("list", "--section", "audio", "--json")
        self.assertEqual(code, 0)
        self.assertTrue(all(s["section"] == "audio" for s in json.loads(out)))
        code, out = run("links", "cairo", "--topic", "egypt", "--commercial")
        self.assertEqual(code, 0)
        self.assertIn("https://www.pexels.com/search/videos/cairo/", out)
        code, out = run("show", "polyhaven")
        self.assertEqual(json.loads(out)["licence"]["name"], "CC0")
        code, out = run("sections")
        self.assertIn("egypt", out)

    def test_probe_offline(self):
        with mock.patch.object(FMC, "probe_one", return_value="ok"), mock.patch.object(FMC.time, "sleep"):
            code, out = run("probe", "--ids", "polyhaven,stokpic")
        self.assertEqual(code, 0)
        self.assertIn("polyhaven", out)
        self.assertIn("was no-dns", out)


if __name__ == "__main__":
    unittest.main()
