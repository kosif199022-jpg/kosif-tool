"""Free footage, offline: the sources database (schema, uniqueness, templates), licence extraction, attribution
formatting, every search adapter against hand-written synthetic answers shaped like each API or page, key gating,
the rate limit, size caps, downloads with sidecars and ATTRIBUTION.md. urlopen is replaced for the whole module,
so nothing leaves the machine.

    python3 -m unittest discover -s .claude/skills/kosif-superpowers/evals -p 'test_free_footage.py' -v
"""
import datetime
import email.message
import email.utils
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import urllib.error
import urllib.parse
from http.client import IncompleteRead, InvalidURL
from pathlib import Path
from unittest import mock

SK = Path(__file__).resolve().parents[1]
SCRIPT = SK / "scripts" / "free_footage.py"
FIX = SK / "evals" / "fixtures" / "free_footage"
sys.path.insert(0, str(SK / "scripts"))
import free_footage as FF  # noqa: E402

MP4 = b"\x00\x00\x00\x18ftypmp42\x00\x00\x00\x00mp42isom" + b"\x00" * 4000
NO_KEYS = {k: "" for k in FF.KEY_ENV.values()}
_PATCH = None


def setUpModule():
    global _PATCH
    _PATCH = mock.patch("urllib.request.urlopen", side_effect=AssertionError("a test tried to reach the network"))
    _PATCH.start()


def tearDownModule():
    _PATCH.stop()


def fixture(name, binary=False):
    p = FIX / name
    return p.read_bytes() if binary else p.read_text(encoding="utf-8")


class Headers(dict):
    def get(self, key, default=None):
        for k, v in self.items():
            if k.lower() == key.lower():
                return v
        return default


class Resp:
    def __init__(self, url, status, body, headers):
        self.url, self.status, self._body, self._pos = url, status, body, 0
        self.headers = Headers(headers)

    def read(self, n=-1):
        if n is None or n < 0:
            n = len(self._body) - self._pos
        chunk = self._body[self._pos:self._pos + n]
        self._pos += len(chunk)
        return chunk

    def close(self):
        pass

    def geturl(self):
        return self.url


class Failing(Resp):
    """A response whose body breaks after `good` bytes, the way a stalled or reset connection does."""

    def __init__(self, url, body, headers, error, good=0):
        super().__init__(url, 200, body, headers)
        self.error, self.good = error, good

    def read(self, n=-1):
        if self._pos >= self.good:
            raise self.error
        return super().read(min(n, self.good - self._pos) if n and n > 0 else self.good - self._pos)


class Transport:
    """Routes a request URL (regex) to (status, body, headers); records every call; refuses unknown URLs. Like
    http.client, it refuses a URL with raw spaces or control characters (InvalidURL) before anything is sent."""

    def __init__(self, routes):
        self.routes = list(routes)
        self.calls = []

    def __call__(self, req, timeout):
        url = req.full_url
        self.calls.append((url, dict(req.header_items()), timeout))
        if re.search(r"[\x00-\x20\x7f]", url):
            raise InvalidURL(f"URL can't contain control characters. {url!r}")
        for rx, answer in self.routes:
            if re.search(rx, url):
                if callable(answer):
                    answer = answer(req)
                if isinstance(answer, Resp):
                    return answer
                status, body, headers = (list(answer) + [{}])[:3] if isinstance(answer, tuple) else (200, answer, {})
                body = body.encode("utf-8") if isinstance(body, str) else body
                if status >= 400:
                    hdrs = email.message.Message()
                    for k, v in (headers or {}).items():
                        hdrs[k] = v
                    raise urllib.error.HTTPError(url, status, "error", hdrs, io.BytesIO(body))
                return Resp(url, status, body, headers or {})
        raise AssertionError(f"unexpected request {url}")

    def urls(self):
        return [c[0] for c in self.calls]


def http(routes, delay=0.0):
    sleeps = []
    t = Transport(routes)
    h = FF.Http(delay=delay, timeout=5, transport=t, sleep=sleeps.append, clock=lambda: 0.0)
    return h, t, sleeps


DB = FF.load_db()


def archive_meta(req):
    """The metadata fixture, re-labelled per item with the licence its search record carries."""
    ident = urllib.parse.unquote(req.full_url.rsplit("/", 1)[-1])
    docs = {d["identifier"]: d for d in json.loads(fixture("archive_search.json"))["response"]["docs"]}
    meta = json.loads(fixture("archive_meta.json"))
    meta["metadata"].update(identifier=ident, licenseurl=docs.get(ident, {}).get("licenseurl"))
    return (200, json.dumps(meta), {})


ROUTES = [
    (r"commons\.wikimedia\.org/w/api\.php", fixture("wikimedia_search.json")),
    (r"archive\.org/advancedsearch\.php", fixture("archive_search.json")),
    (r"archive\.org/metadata/", archive_meta),
    (r"images-api\.nasa\.gov/search", fixture("nasa_search.json")),
    (r"images-api\.nasa\.gov/asset/", fixture("nasa_asset.json")),
    (r"metadata\.json$", fixture("nasa_metadata.json")),
    (r"mixkit\.co/free-stock-video/discover/", fixture("mixkit_discover.html")),
    (r"mixkit\.co/free-stock-video/synthetic-night-walk", fixture("mixkit_clip_restricted.html")),
    (r"mixkit\.co/free-stock-video/synthetic-traffic", fixture("mixkit_clip_free.html")),
    (r"coverr\.co/s\?", fixture("coverr_search.html")),
    (r"api\.pexels\.com/videos/search", fixture("pexels_search.json")),
    (r"pixabay\.com/api/videos/", fixture("pixabay_search.json")),
]


# ------------------------------------------------------------------------------------------------- database

class DatabaseTest(unittest.TestCase):
    REQUIRED = ("pexels", "pixabay", "mixkit", "coverr", "videvo", "videezy", "vecteezy", "dareful", "mazwai",
                "lifeofvids", "wikimedia", "archive", "nasa", "esa", "openverse", "pinterest")

    def test_database_is_valid(self):
        self.assertEqual(FF.validate_db(DB), [])

    def test_every_requested_source_is_present_once(self):
        ids = [s["id"] for s in DB["sources"]]
        self.assertEqual(len(ids), len(set(ids)))
        names = [s["name"].lower() for s in DB["sources"]]
        self.assertEqual(len(names), len(set(names)))
        for sid in self.REQUIRED:
            self.assertIn(sid, ids)

    def test_pinterest_is_not_a_licence_source(self):
        p = FF.sources_by_id(DB)["pinterest"]
        self.assertFalse(p["licence_source"])
        self.assertIn("not a licence source", p["licence"]["name"].lower())
        self.assertIn("credit/link only", p["licence"]["name"].lower())
        self.assertEqual((p["commercial_use"], p["tool"]["download"]), ("n/a", "none"))

    def test_keys_are_named_never_stored(self):
        by = FF.sources_by_id(DB)
        self.assertEqual(by["pexels"]["api"]["key_env"], "PEXELS_API_KEY")
        self.assertEqual(by["pixabay"]["api"]["key_env"], "PIXABAY_API_KEY")
        for s in DB["sources"]:
            self.assertEqual(s["tool"]["search"] == "api-key", s["id"] in FF.KEY_ENV, s["id"])
        sec = FF._sibling("_secrets")
        self.assertEqual(sec.scan_object(DB), [])

    def test_reachability_recorded_for_the_sandbox_run(self):
        by = FF.sources_by_id(DB)
        expect = {"wikimedia": "partial", "archive": "ok", "nasa": "ok", "mixkit": "ok", "coverr": "ok",
                  "dareful": "ok", "videezy": "ok", "vecteezy": "ok", "openverse": "ok", "pexels": "needs-key",
                  "pixabay": "needs-key", "lifeofvids": "timeout", "storyblocks": "paid"}
        for sid, status in expect.items():
            self.assertEqual(by[sid]["reachability"]["status"], status, sid)
            self.assertEqual(by[sid]["reachability"]["checked_on"], "2026-10-29")
        self.assertIn("images", by["openverse"]["video_kinds"][0])

    def test_schema_file_matches_the_validator(self):
        schema = json.loads(FF.SCHEMA_PATH.read_text(encoding="utf-8"))
        src = schema["$defs"]["source"]
        self.assertEqual(set(src["required"]), set(FF.REQUIRED_SOURCE))
        self.assertEqual(set(schema["required"]), set(FF.REQUIRED_TOP))
        for key, keys in FF.REQUIRED_NESTED.items():
            self.assertEqual(set(src["properties"][key]["required"]), set(keys), key)
        for key, allowed in FF.ENUMS.items():
            a, _, b = key.partition(".")
            node = src["properties"][a]["properties"][b] if b else src["properties"][a]
            self.assertEqual(tuple(node["enum"]), allowed, key)
        self.assertEqual(schema["properties"]["schema"]["const"], FF.DB_SCHEMA)

    def test_validator_catches_broken_records(self):
        bad = json.loads(json.dumps(DB))
        bad["sources"][1]["id"] = bad["sources"][0]["id"]
        bad["sources"][2]["commercial_use"] = "maybe"
        bad["sources"][3]["attribution"]["template"] = "{title} by {creator}"
        bad["sources"][4]["search_url"] = "https://example.org/search"
        pex = next(s for s in bad["sources"] if s["id"] == "pexels")
        pex["api"]["key_env"] = None
        pin = next(s for s in bad["sources"] if s["id"] == "pinterest")
        pin["tool"]["download"] = "direct"
        bad["sources"][5]["surprise"] = 1
        errs = "\n".join(FF.validate_db(bad))
        for needle in ("duplicate id", "commercial_use must be one of", "unknown placeholders ['creator']",
                       "{query} placeholder", "api-key needs", "not a licence source", "unknown keys ['surprise']"):
            self.assertIn(needle, errs)

    def test_every_template_renders_cleanly(self):
        full = dict(title="T", author="A", source="S", licence="L", licence_url="https://l", page_url="https://p")
        for s in DB["sources"]:
            tpl = s["attribution"]["template"]
            for fields in (full, {**full, "author": None}, {**full, "licence_url": None, "author": None}):
                out = FF.format_attribution(tpl, **fields)
                with self.subTest(source=s["id"], fields=fields):
                    self.assertNotIn("{", out)
                    self.assertNotIn("()", out)
                    self.assertNotRegex(out, r"by\s*[,:]|,\s*,|\s[,:;]")
                    self.assertIn("https://p", out)


# ------------------------------------------------------------------------------------------------- licences

class LicenceTest(unittest.TestCase):
    def check(self, rec, name, att, com, der, sa=None):
        self.assertEqual(rec["name"], name)
        self.assertEqual((rec["attribution_required"], rec["commercial"], rec["derivatives"]), (att, com, der))
        if sa is not None:
            self.assertEqual(rec["share_alike"], sa)

    def test_creative_commons_urls(self):
        self.check(FF.classify_licence(None, "https://creativecommons.org/licenses/by-nc-sa/2.0/"),
                   "CC BY-NC-SA 2.0", True, False, True, True)
        self.check(FF.classify_licence(None, "https://creativecommons.org/licenses/by-nd/4.0/deed.de"),
                   "CC BY-ND 4.0", True, True, False)
        self.check(FF.classify_licence(None, "https://creativecommons.org/licenses/by-sa/3.0/igo"),
                   "CC BY-SA 3.0 IGO", True, True, True, True)
        self.check(FF.classify_licence(None, "https://creativecommons.org/licenses/by/3.0"), "CC BY 3.0", True, True, True)
        zero = FF.classify_licence(None, "http://creativecommons.org/publicdomain/zero/1.0/deed.en")
        self.check(zero, "CC0 1.0", False, True, True)
        self.assertTrue(zero["url"].startswith("https://"))
        self.check(FF.classify_licence(None, "http://creativecommons.org/publicdomain/mark/1.0/"),
                   "Public Domain Mark 1.0", False, True, True)
        self.assertFalse(FF.classify_licence(None, "http://creativecommons.org/licenses/publicdomain/")["attribution_required"])

    def test_short_names(self):
        self.check(FF.classify_licence("CC BY-SA 4.0"), "CC BY-SA 4.0", True, True, True, True)
        self.check(FF.classify_licence("CC-BY-3.0"), "CC BY 3.0", True, True, True)
        self.check(FF.classify_licence("CC0"), "CC0 1.0", False, True, True)
        self.check(FF.classify_licence("Public domain"), "Public domain", False, True, True)
        unknown = FF.classify_licence("All rights reserved")
        self.assertFalse(unknown["verified"])
        self.assertIsNone(unknown["commercial"])

    def test_mixkit_notices(self):
        free, restricted, unknown = (FF.mixkit_licence(n) for n in ("Free", "Mixkit Restricted License", None))
        self.assertEqual((free["name"], free["commercial"]), (FF.MIXKIT_FREE, True))
        self.assertEqual((restricted["name"], restricted["commercial"]), (FF.MIXKIT_RESTRICTED, False))
        self.assertIn("personal use only", restricted["note"])
        self.assertIsNone(unknown["commercial"])
        self.assertFalse(unknown["verified"])

    def test_page_notice_reads_json_ld_or_the_download_box(self):
        self.assertEqual(FF.mixkit_page_notice(fixture("mixkit_clip_restricted.html")), "Mixkit Restricted License")
        self.assertEqual(FF.mixkit_page_notice(fixture("mixkit_clip_free.html")), "Free")
        self.assertIsNone(FF.mixkit_page_notice("<html></html>"))


# ------------------------------------------------------------------------------------------------- attribution

class AttributionTest(unittest.TestCase):
    def test_full_tasl_line_from_the_commons_template(self):
        tpl = FF.sources_by_id(DB)["wikimedia"]["attribution"]["template"]
        out = FF.format_attribution(tpl, title="Harbour", author='<a href="//x">Example &amp; Maker</a>',
                                    licence="CC BY-SA 4.0", licence_url="https://creativecommons.org/licenses/by-sa/4.0",
                                    page_url="https://commons.wikimedia.org/wiki/File:H.webm")
        self.assertEqual(out, '"Harbour" by Example & Maker, CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0), '
                              "via Wikimedia Commons: https://commons.wikimedia.org/wiki/File:H.webm")

    def test_missing_fields_drop_their_fragment(self):
        by = FF.sources_by_id(DB)
        self.assertEqual(FF.format_attribution(by["pexels"]["attribution"]["template"], page_url="https://p"),
                         "Video from Pexels: https://p")
        self.assertEqual(FF.format_attribution(by["nasa"]["attribution"]["template"], title="Orbit", page_url="https://n"),
                         '"Orbit", courtesy NASA: https://n')
        pin = FF.format_attribution(by["pinterest"]["attribution"]["template"], page_url="https://pin")
        self.assertIn("original creator: unknown (trace it)", pin)
        self.assertTrue(FF.format_attribution(None, page_url="https://x").startswith("Untitled clip"))


# ------------------------------------------------------------------------------------------------- parsers

class ParserTest(unittest.TestCase):
    def test_wikimedia(self):
        rows = FF.parse_wikimedia(DB, json.loads(fixture("wikimedia_search.json")))
        self.assertEqual([r["id"] for r in rows], ["wikimedia:9000001", "wikimedia:9000002"])  # by index, audio skipped
        cc0, bysa = rows
        self.assertEqual(cc0["licence"]["name"], "CC0 1.0")
        self.assertFalse(cc0["licence"]["attribution_required"])
        self.assertEqual(bysa["licence"]["name"], "CC BY-SA 4.0")
        self.assertTrue(bysa["licence"]["share_alike"])
        self.assertEqual(bysa["author"], "Example & Filmmaker")
        self.assertNotIn("utm_", bysa["file_url"])
        self.assertEqual((bysa["width"], bysa["height"], bysa["duration"]), (1080, 1920, 12.5))
        self.assertIn("via Wikimedia Commons", bysa["attribution"])

    def test_commons_title_from_links(self):
        t = FF.commons_title_from_url
        self.assertEqual(t("https://commons.wikimedia.org/wiki/File:Ocean in Sommaroy.webm"), "File:Ocean_in_Sommaroy.webm")
        self.assertEqual(t("https://upload.wikimedia.org/wikipedia/commons/5/5d/Ocean_in_Sommaroy.webm"),
                         "File:Ocean_in_Sommaroy.webm")
        self.assertEqual(t("https://upload.wikimedia.org/wikipedia/commons/transcoded/5/5d/A.webm/A.webm.720p.vp9.webm"),
                         "File:A.webm")
        self.assertIsNone(t("https://example.org/File:A.webm"))

    def test_archive(self):
        docs = FF.parse_archive_search(json.loads(fixture("archive_search.json")))
        self.assertEqual(len(docs), 3)
        meta = json.loads(fixture("archive_meta.json"))
        best = FF.pick_archive_file(meta["files"])
        self.assertEqual(best["name"], "Coast Film Original.mov")
        small = FF.pick_archive_file(meta["files"], max_bytes=20 * 1048576)
        self.assertEqual(small["name"], "Coast Film Original.mp4")
        r = FF.archive_result(DB, docs[0], meta, 20 * 1048576)
        self.assertEqual(r["file_url"], "https://archive.org/download/synthetic-coast-film/Coast%20Film%20Original.mp4")
        self.assertEqual(r["licence"]["name"], "CC BY 4.0")
        self.assertEqual(r["author"], "Example Archive Group, Second Maker")
        full = FF.archive_result(DB, docs[0], meta)
        self.assertEqual(full["duration"], 83.0)  # "00:01:23"
        nd = FF.archive_result(DB, docs[1], meta)
        self.assertFalse(nd["licence"]["derivatives"])
        self.assertEqual(FF.archive_result(DB, docs[2], meta)["licence"]["name"], "Public Domain Mark 1.0")
        self.assertIn("licenseurl:*", urllib.parse.unquote_plus(FF.archive_search_url("sea", 5)))
        q = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(FF.archive_search_url("sea", 5, any_licence=True)).query))
        self.assertEqual(q["q"], "(sea) AND mediatype:(movies)")

    def test_nasa(self):
        docs = FF.parse_nasa_search(json.loads(fixture("nasa_search.json")))
        self.assertEqual([d["nasa_id"] for d in docs], ["SYNTH_20260101_Ocean_Orbit"])  # the image is skipped
        vids, meta = FF.nasa_variants(json.loads(fixture("nasa_asset.json")))
        self.assertTrue(vids[0].endswith("~orig.mp4") and vids[1].endswith("~large.mp4") and vids[2].endswith("~medium.mp4"))
        self.assertTrue(all(v.startswith("https://") for v in vids) and meta.startswith("https://"))
        self.assertFalse(any("~preview" in v for v in vids))
        dims = FF.parse_nasa_metadata(json.loads(fixture("nasa_metadata.json")))
        self.assertEqual(dims, {"width": 3840, "height": 2160, "duration": 65.0})
        r = FF.nasa_result(DB, docs[0], vids[0], dims, vids)
        self.assertEqual(r["attribution"], '"Synthetic ocean from orbit", courtesy NASA (Example Visualizer): '
                                           "https://images.nasa.gov/details/SYNTH_20260101_Ocean_Orbit")
        self.assertTrue(r["licence"]["attribution_required"])
        self.assertEqual(len(r["alternates"]), 2)

    def test_pexels_and_pixabay(self):
        px = FF.parse_pexels(DB, json.loads(fixture("pexels_search.json")))
        self.assertEqual(px[0]["file_url"].rsplit("/", 1)[-1], "1000001-uhd_2160_3840_25fps.mp4")
        self.assertEqual((px[0]["width"], px[0]["height"], px[0]["title"]), (2160, 3840, "Synthetic night street in the rain"))
        self.assertEqual(px[0]["attribution"],
                         "Video by Example Videographer from Pexels: https://www.pexels.com/video/synthetic-night-street-in-the-rain-1000001/")
        self.assertEqual(px[1]["title"], "Pexels clip")
        pb = FF.parse_pixabay(DB, json.loads(fixture("pixabay_search.json")))
        self.assertTrue(pb[0]["file_url"].endswith("2000001-medium.mp4"))  # 'large' is empty
        self.assertEqual((pb[0]["height"], pb[0]["author"]), (720, "example_pixabay_user"))
        self.assertEqual(pb[1]["title"], "Pixabay clip")
        self.assertFalse(pb[0]["licence"]["attribution_required"])

    def test_mixkit_tag_page_with_json_ld(self):
        rows = FF.parse_mixkit(DB, fixture("mixkit_tag.html"))
        self.assertEqual([r["id"] for r in rows], ["mixkit:30001", "mixkit:30002", "mixkit:30003"])
        self.assertEqual(rows[0]["licence"]["name"], FF.MIXKIT_RESTRICTED)
        self.assertFalse(rows[0]["licence"]["commercial"])
        self.assertEqual(rows[0]["duration"], 16.0)
        self.assertEqual(rows[1]["licence"]["name"], FF.MIXKIT_FREE)
        self.assertEqual(rows[2]["title"], "Synthetic tide pool")
        self.assertFalse(rows[2]["licence"]["verified"])
        self.assertEqual(rows[0]["file_url"], "https://assets.mixkit.co/videos/30001/30001-720.mp4")
        self.assertNotIn("alternates", rows[0])  # Restricted: the 720p file only (larger files answer 403)
        self.assertEqual(rows[0]["page_url"], "https://mixkit.co/free-stock-video/synthetic-gulls-over-the-sea-30001/")
        self.assertEqual((rows[0]["width"], rows[0]["height"]), (1280, 720))
        free = rows[1]  # Free: 2160p first, then 1080p, then 720p; sized at the 1080p a Free clip is known to have
        self.assertEqual(free["file_url"], "https://assets.mixkit.co/videos/30002/30002-2160.mp4")
        self.assertEqual(free["alternates"], ["https://assets.mixkit.co/videos/30002/30002-1080.mp4",
                                              "https://assets.mixkit.co/videos/30002/30002-720.mp4"])
        self.assertEqual((free["quality"], free["width"], free["height"]), (1080, 1920, 1080))
        self.assertEqual(rows[2]["file_url"], "https://assets.mixkit.co/videos/30003/30003-720.mp4")  # not read yet

    def test_mixkit_discover_page_titles_and_orientation(self):
        rows = FF.parse_mixkit(DB, fixture("mixkit_discover.html"))
        self.assertEqual([r["title"] for r in rows], ["Synthetic night walk in a big city", "Synthetic traffic from above"])
        self.assertEqual((rows[0]["width"], rows[0]["height"]), (720, 1280))  # 460x818 thumbnail = 9:16
        self.assertEqual(FF.orientation_of(rows[0]), "portrait")
        self.assertIn("size-from-thumbnail", rows[0]["flags"])
        self.assertIn("licence-checked-at-download", rows[0]["flags"])

    def test_coverr_page_state(self):
        rows, premium = FF.parse_coverr(DB, fixture("coverr_search.html"))
        self.assertEqual(premium, 1)
        self.assertEqual([r["id"] for r in rows], ["coverr:AAAA111111", "coverr:BBBB222222", "coverr:DDDD444444"])
        calm, vertical, ai = rows
        self.assertEqual((calm["width"], calm["height"]), (1920, 1080))
        self.assertEqual((vertical["width"], vertical["height"]), (1920, 3412))  # measured on a real 1152x2048 clip
        self.assertIn("upscaled-file", vertical["flags"])
        self.assertEqual(vertical["author"], "Example Wave Shooter")
        self.assertIn("ai-generated", ai["flags"])
        self.assertEqual(ai["author"], "ai_user_1")
        dumped = json.dumps(rows)
        self.assertNotIn("@example.com", dumped)  # personal fields are never copied
        self.assertEqual(calm["title"], "Synthetic calm waves")
        self.assertEqual(calm["page_url"], "https://coverr.co/videos/synthetic-calm-waves-aaaa111111")
        with self.assertRaises(FF.FootageError):
            FF.parse_coverr(DB, "<html>blocked</html>")
        empty = re.sub(r'"hits":\[.*\]\}\}</script>', '"hits":[]}}</script>', fixture("coverr_search.html"), flags=re.S)
        self.assertIn('"hits":[]', empty)
        self.assertEqual(FF.parse_coverr(DB, empty), ([], 0))  # never the site's cover video as a "result"


# ------------------------------------------------------------------------------------------------- keys, search

class KeyGatingTest(unittest.TestCase):
    def test_default_sources_follow_the_environment(self):
        self.assertNotIn("pexels", FF.default_sources(DB, NO_KEYS))
        self.assertNotIn("pixabay", FF.default_sources(DB, NO_KEYS))
        self.assertEqual(set(FF.default_sources(DB, NO_KEYS)), {"wikimedia", "archive", "nasa", "mixkit", "coverr"})
        both = FF.default_sources(DB, {"PEXELS_API_KEY": "abc", "PIXABAY_API_KEY": "def"})
        self.assertTrue({"pexels", "pixabay"} <= set(both))

    def test_keyed_source_without_key_is_skipped_without_a_request(self):
        h, t, _ = http([])
        with mock.patch.dict(os.environ, NO_KEYS):
            rep = FF.run_search(h, DB, "sea", ["pexels", "pixabay"], 3, {})
        self.assertEqual(t.calls, [])
        self.assertEqual(rep["sources"]["pexels"]["status"], "skipped")
        self.assertIn("PEXELS_API_KEY", rep["sources"]["pexels"]["detail"])
        self.assertIn("PIXABAY_API_KEY", rep["sources"]["pixabay"]["detail"])

    def test_keys_are_sent_but_never_reported(self):
        secret_px, secret_pb = "pxTESTKEY0123456789", "pbTESTKEY9876543210"
        routes = [(r"api\.pexels\.com", fixture("pexels_search.json")), (r"pixabay\.com/api", (400, "[ERROR 400] bad key"))]
        h, t, _ = http(routes)
        with mock.patch.dict(os.environ, {"PEXELS_API_KEY": secret_px, "PIXABAY_API_KEY": secret_pb}):
            rep = FF.run_search(h, DB, "sea", ["pexels", "pixabay"], 3, {})
            self.assertNotIn(secret_pb, FF.redact(f"https://pixabay.com/api/videos/?key={secret_pb}&q=x"))
        px_call = next(c for c in t.calls if "pexels" in c[0])
        self.assertEqual(px_call[1].get("Authorization"), secret_px)
        self.assertIn(secret_pb, next(c[0] for c in t.calls if "pixabay" in c[0]))
        self.assertEqual(rep["sources"]["pixabay"]["status"], "error")
        text = json.dumps(rep)
        self.assertNotIn(secret_pb, text)
        self.assertNotIn(secret_px, text)
        self.assertIn("key=***", rep["sources"]["pixabay"]["detail"])


class SearchTest(unittest.TestCase):
    SOURCES = ["wikimedia", "archive", "nasa", "mixkit", "coverr"]

    def run_all(self, opts, sources=None, routes=ROUTES):
        h, t, _ = http(routes)
        with mock.patch.dict(os.environ, NO_KEYS):
            return FF.run_search(h, DB, "sea", sources or self.SOURCES, 10, opts), t

    def test_every_keyless_adapter_and_the_nd_default(self):
        rep, t = self.run_all({})
        self.assertEqual({k: v["status"] for k, v in rep["sources"].items()}, {s: "ok" for s in self.SOURCES})
        ids = {r["id"] for r in rep["results"]}
        self.assertIn("archive:synthetic-coast-film", ids)
        self.assertNotIn("archive:synthetic-nd-reel", ids)  # ND dropped: a montage is an edit
        self.assertEqual(rep["sources"]["archive"]["dropped"], {"no-derivatives licence (a montage is an edit)": 1})
        self.assertTrue(all(r["query"] == "sea" for r in rep["results"]))
        self.assertIn("coverr: skipped 1 premium (Coverr+) clips", rep["warnings"])
        self.assertEqual(rep["schema"], FF.RESULTS_SCHEMA)
        self.assertFalse(any("metadata.json" in u for u in t.urls()))  # NASA sizes only when a filter needs them
        self.assertTrue(any("filetype%3Avideo" in u for u in t.urls()))

    def test_filters(self):
        rep, t = self.run_all({"orientation": "portrait"})
        self.assertTrue(rep["results"])
        self.assertTrue(all(FF.orientation_of(r) == "portrait" for r in rep["results"]))
        rep, t = self.run_all({"min_height": 1900})
        hs = {r["id"]: r["height"] for r in rep["results"]}
        self.assertEqual(hs.get("nasa:SYNTH_20260101_Ocean_Orbit"), 2160)  # metadata.json was read for the filter
        self.assertIn("wikimedia:9000002", hs)
        self.assertIn("coverr:BBBB222222", hs)  # file 1920x3412, source 1152x2048: 2048 >= 1900
        rep2, _ = self.run_all({"min_height": 2100})
        self.assertNotIn("coverr:BBBB222222", {r["id"] for r in rep2["results"]})  # the upscale adds no detail
        rep, _ = self.run_all({"commercial": True, "no_ai": True})
        for r in rep["results"]:
            self.assertIs(r["licence"]["commercial"], True, r["id"])
            self.assertNotIn("ai-generated", r["flags"])
        rep, _ = self.run_all({"allow_nd": True})
        self.assertIn("archive:synthetic-nd-reel", {r["id"] for r in rep["results"]})

    def test_commercial_filter_reads_mixkit_clip_pages(self):
        rep, t = self.run_all({"commercial": True}, ["mixkit"])
        self.assertEqual([r["id"] for r in rep["results"]], ["mixkit:40002"])  # 40001 is Restricted
        self.assertEqual(rep["results"][0]["licence"]["name"], FF.MIXKIT_FREE)
        self.assertEqual(sum("free-stock-video/synthetic" in u for u in t.urls()), 2)
        rep, t = self.run_all({"commercial": True, "orientation": "landscape"}, ["mixkit"])
        self.assertEqual([r["id"] for r in rep["results"]], ["mixkit:40002"])
        self.assertEqual(sum("free-stock-video/synthetic" in u for u in t.urls()), 1)  # the portrait clip is not opened

    def test_one_broken_source_does_not_stop_the_others(self):
        routes = [(r"images-api\.nasa\.gov", (503, "down")), (r"coverr\.co", "<html>no state</html>"),
                  (r"archive\.org/advancedsearch", "<html>not json</html>")] + ROUTES
        rep, _ = self.run_all({}, routes=routes)
        st = rep["sources"]
        self.assertEqual((st["nasa"]["status"], st["coverr"]["status"], st["archive"]["status"]), ("error", "error", "error"))
        self.assertIn("503", st["nasa"]["detail"])
        self.assertIn("ng-state", st["coverr"]["detail"])
        self.assertIn("did not return JSON", st["archive"]["detail"])
        self.assertEqual(st["wikimedia"]["status"], "ok")
        self.assertEqual(st["mixkit"]["status"], "ok")

    def test_limit_per_source(self):
        h, _, _ = http(ROUTES)
        rep = FF.run_search(h, DB, "sea", ["coverr"], 1, {})
        self.assertEqual(len(rep["results"]), 1)
        self.assertEqual(rep["sources"]["coverr"]["found"], 3)


# ------------------------------------------------------------------------------------------------- HTTP

class HttpTest(unittest.TestCase):
    def test_rate_limit_per_host(self):
        t = Transport([(r".", "{}")])
        now = [100.0]
        sleeps = []
        h = FF.Http(delay=1.5, transport=t, sleep=lambda s: (sleeps.append(s), now.__setitem__(0, now[0] + s)),
                    clock=lambda: now[0])
        h.get_json("https://a.example/1")
        h.get_json("https://b.example/1")
        self.assertEqual(sleeps, [])
        now[0] += 0.5
        h.get_json("https://a.example/2")
        self.assertEqual(len(sleeps), 1)
        self.assertAlmostEqual(sleeps[0], 1.0)
        ua = t.calls[0][1].get("User-agent")
        self.assertTrue(ua.startswith("KOSIF-free-footage/"))
        self.assertEqual(t.calls[0][2], 20.0)  # the default timeout is always passed

    def test_429_retry_after(self):
        answers = iter([(429, "slow down", {"Retry-After": "2"}), (200, "{\"ok\": true}")])
        h, t, sleeps = http([(r".", lambda req: next(answers))])
        self.assertEqual(h.get_json("https://x.example/"), {"ok": True})
        self.assertIn(2.0, sleeps)
        h2, _, sleeps2 = http([(r".", (429, "no", {"Retry-After": "600"}))])
        with self.assertRaisesRegex(FF.HttpError, "too long"):
            h2.get_json("https://x.example/")
        self.assertEqual(sleeps2, [])  # never waits ten minutes

    def test_page_cap(self):
        h, _, _ = http([(r"big", (200, b"x" * 10, {"Content-Length": str(50 * 1048576)})), (r"long", b"y" * 3000)])
        with self.assertRaisesRegex(FF.FootageError, "page cap"):
            h.get_bytes("https://x.example/big", cap_mb=40)
        with self.assertRaisesRegex(FF.FootageError, "page cap"):
            h.get_bytes("https://x.example/long", cap_mb=0.001)

    def test_network_errors_become_footage_errors(self):
        def boom(req, timeout):
            raise urllib.error.URLError(TimeoutError("timed out"))
        h = FF.Http(delay=0, transport=boom, sleep=lambda s: None)
        with self.assertRaises(FF.HttpError) as cm:
            h.get_text("https://slow.example/")
        self.assertIn("timed out", str(cm.exception))


# ------------------------------------------------------------------------------------------------- download

class DownloadTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.out = self.dir / "clips"
        h, _, _ = http(ROUTES)
        with mock.patch.dict(os.environ, NO_KEYS):
            rep = FF.run_search(h, DB, "sea", ["wikimedia", "archive", "nasa", "mixkit", "coverr"], 10, {"allow_nd": True})
        self.results = self.dir / "last_search.json"
        self.results.write_text(json.dumps(rep), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def opts(self, **kw):
        base = {"results": self.results, "max_mb": 50, "max_bytes": 50 * 1048576}
        base.update(kw)
        return base

    def test_result_id_download_writes_sidecar_and_credits(self):
        h, t, _ = http([(r"upload\.wikimedia\.org", (200, MP4, {"Content-Type": "video/webm"}))] + ROUTES)
        with mock.patch.object(FF, "measure", return_value={"width": 1080, "height": 1920}):
            r = FF.download_one(h, DB, "wikimedia:9000002", self.out, self.opts())
        media = self.out / r["file"]
        self.assertEqual(media.name, "wikimedia-9000002.webm")
        self.assertEqual(media.read_bytes(), MP4)
        side = json.loads(FF.sidecar_for(media).read_text(encoding="utf-8"))
        self.assertEqual(side["schema"], FF.ASSET_SCHEMA)
        self.assertEqual(side["licence"]["name"], "CC BY-SA 4.0")
        self.assertEqual(side["bytes"], len(MP4))
        self.assertEqual(len(side["sha256"]), 64)
        self.assertEqual(side["measured"], {"width": 1080, "height": 1920})
        credits = (self.out / "ATTRIBUTION.md").read_text(encoding="utf-8")
        self.assertIn("| wikimedia-9000002.webm | Wikimedia Commons | CC BY-SA 4.0 | yes | yes |", credits)
        self.assertIn('- "Synthetic harbour at dusk" by Example & Filmmaker, CC BY-SA 4.0', credits)
        n = len(t.calls)
        with mock.patch.object(FF, "measure", return_value={}):
            again = FF.download_one(h, DB, "wikimedia:9000002", self.out, self.opts())
        self.assertTrue(again["reused"])
        self.assertEqual(len(t.calls), n)  # the file is not fetched twice
        self.assertFalse(list(self.out.glob("*.part")))

    def test_credits_accumulate_and_rebuild(self):
        h, _, _ = http([(r"cdn\.coverr\.co", (200, MP4, {"Content-Type": "video/mp4"})),
                        (r"archive\.org/download", (200, MP4, {"Content-Type": "video/mp4"}))] + ROUTES)
        with mock.patch.object(FF, "measure", return_value={}):
            FF.download_one(h, DB, "coverr:AAAA111111", self.out, self.opts())
            FF.download_one(h, DB, "archive:synthetic-coast-film", self.out, self.opts())
        text = FF.credits_markdown(self.out)
        self.assertEqual(text.count("\n- "), 2)
        self.assertIn("*(optional)*", text)  # Coverr does not require credit
        self.assertIn("via the Internet Archive", text)
        (self.out / "coverr-AAAA111111.mp4").unlink()
        (self.out / "coverr-AAAA111111.mp4.json").unlink()
        FF.write_credits(self.out)
        self.assertNotIn("Coverr", (self.out / "ATTRIBUTION.md").read_text(encoding="utf-8"))

    def test_archive_picks_the_derivative_under_the_cap(self):
        h, t, _ = http([(r"archive\.org/download", (200, MP4, {"Content-Type": "video/mp4"}))] + ROUTES)
        with mock.patch.object(FF, "measure", return_value={}):
            r = FF.download_one(h, DB, "archive:synthetic-coast-film", self.out, self.opts(max_mb=20))
        self.assertEqual(r["file"], "archive-synthetic-coast-film.mp4")
        self.assertTrue(any(u.endswith("Coast%20Film%20Original.mp4") for u in t.urls()))

    def test_size_cap_and_html_answers_leave_nothing_behind(self):
        big = (200, MP4, {"Content-Type": "video/mp4", "Content-Length": str(80 * 1048576)})
        h, _, _ = http([(r"cdn\.coverr\.co", big)] + ROUTES)
        with self.assertRaisesRegex(FF.FootageError, "over --max-mb"):
            FF.download_one(h, DB, "coverr:AAAA111111", self.out, self.opts())
        h, _, _ = http([(r"cdn\.coverr\.co", (200, "<!doctype html><title>Sign in</title>", {"Content-Type": "text/html"}))] + ROUTES)
        with self.assertRaisesRegex(FF.FootageError, "not a video"):
            FF.download_one(h, DB, "coverr:AAAA111111", self.out, self.opts())
        h, _, _ = http([(r"cdn\.coverr\.co", (200, MP4 * 400, {"Content-Type": "video/mp4"}))] + ROUTES)
        with self.assertRaisesRegex(FF.FootageError, "larger than --max-mb"):
            FF.download_one(h, DB, "coverr:AAAA111111", self.out, self.opts(max_mb=0.5))
        self.assertEqual([p.name for p in self.out.iterdir()] if self.out.exists() else [], [])

    def test_nasa_falls_back_to_a_smaller_variant(self):
        over = (200, MP4, {"Content-Type": "video/mp4", "Content-Length": str(400 * 1048576)})
        h, t, _ = http([(r"~orig\.mp4", over), (r"~large\.mp4", (200, MP4, {"Content-Type": "video/mp4"}))] + ROUTES)
        with mock.patch.object(FF, "measure", return_value={}):
            r = FF.download_one(h, DB, "nasa:SYNTH_20260101_Ocean_Orbit", self.out, self.opts())
        side = json.loads(FF.sidecar_for(self.out / r["file"]).read_text(encoding="utf-8"))
        self.assertIn("smaller-variant", side["result"]["flags"])
        self.assertTrue(side["result"]["file_url"].endswith("~large.mp4"))

    def test_mixkit_licence_is_read_from_the_clip_page(self):
        h, _, _ = http([(r"assets\.mixkit\.co", (200, MP4, {"Content-Type": "video/mp4"}))] + ROUTES)
        with self.assertRaisesRegex(FF.FootageError, "commercial"):
            FF.download_one(h, DB, "mixkit:40001", self.out, self.opts(commercial=True))
        with mock.patch.object(FF, "measure", return_value={}):
            r = FF.download_one(h, DB, "mixkit:40001", self.out, self.opts())
        side = json.loads(FF.sidecar_for(self.out / r["file"]).read_text(encoding="utf-8"))
        self.assertEqual(side["licence"]["name"], FF.MIXKIT_RESTRICTED)
        self.assertIn("personal use only", side["licence"]["note"])
        self.assertEqual(side["result"]["duration"], 11.0)
        self.assertNotIn("licence-checked-at-download", side["result"]["flags"])

    def test_nd_refused_unless_allowed(self):
        h, _, _ = http([(r"archive\.org/download", (200, MP4, {"Content-Type": "video/mp4"}))] + ROUTES)
        with self.assertRaisesRegex(FF.FootageError, "forbids edits"):
            FF.download_one(h, DB, "archive:synthetic-nd-reel", self.out, self.opts())
        with mock.patch.object(FF, "measure", return_value={}):
            FF.download_one(h, DB, "archive:synthetic-nd-reel", self.out, self.opts(allow_nd=True))

    def test_unknown_links_need_licence_evidence(self):
        url = "https://files.example.org/clips/sunset.mp4"
        h, _, _ = http([(r"files\.example\.org", (200, MP4, {"Content-Type": "video/mp4"}))])
        with self.assertRaisesRegex(FF.FootageError, "--licence NAME --licence-url URL"):
            FF.download_one(h, DB, url, self.out, self.opts())
        with mock.patch.object(FF, "measure", return_value={}):
            r = FF.download_one(h, DB, url, self.out, self.opts(licence="CC BY 4.0", author="Example Shooter",
                                licence_url="https://creativecommons.org/licenses/by/4.0/", title="Sunset"))
        side = json.loads(FF.sidecar_for(self.out / r["file"]).read_text(encoding="utf-8"))
        self.assertFalse(side["licence"]["verified"])
        self.assertIn("user-supplied", side["licence"]["note"])
        self.assertIn('"Sunset" by Example Shooter, CC BY 4.0', side["attribution"])

    def test_dareful_link_is_labelled_with_its_source(self):
        rec = FF.manual_record(DB, "https://dareful.com/wp-content/clip.mp4",
                               {"licence": "CC BY 4.0", "licence_url": "https://creativecommons.org/licenses/by/4.0/"})
        self.assertEqual(rec["source"], "dareful")
        self.assertIn("courtesy of Dareful", rec["attribution"])
        self.assertEqual(FF.manual_record(DB, "https://notdareful.com/c.mp4",
                                          {"licence": "CC0", "licence_url": "https://creativecommons.org/publicdomain/zero/1.0/"})["source"], "manual")

    def test_pinterest_is_refused(self):
        h, t, _ = http([])
        for url in ("https://www.pinterest.com/pin/123456789/", "https://pin.it/abc", "https://v1.pinimg.com/videos/x.mp4"):
            with self.assertRaisesRegex(FF.FootageError, "not a licence source"):
                FF.download_one(h, DB, url, self.out, self.opts(licence="CC0", licence_url="https://x"))
        self.assertEqual(t.calls, [])

    def test_pexels_link_without_a_key_uses_the_public_endpoint(self):
        h, t, _ = http([(r"videos\.pexels\.com", (200, MP4, {"Content-Type": "video/mp4"}))])
        sf = FF._sibling("stock_fetch")
        with mock.patch.dict(os.environ, NO_KEYS), \
                mock.patch.object(sf, "resolve_pexels", return_value="https://videos.pexels.com/video-files/9112700/x.mp4") as rp, \
                mock.patch.object(FF, "measure", return_value={}):
            r = FF.download_one(h, DB, "https://www.pexels.com/video/synthetic-rain-on-black-9112700/", self.out, self.opts())
        rp.assert_called_once_with("9112700")
        self.assertEqual(r["licence"], "Pexels License")
        self.assertEqual(r["file"], "pexels-9112700.mp4")

    def test_dry_run_writes_nothing(self):
        def head(req):  # only a HEAD request is allowed: the size is asked, the file is not fetched
            self.assertEqual(req.get_method(), "HEAD")
            return (200, b"", {"Content-Type": "video/mp4", "Content-Length": str(12 * 1048576)})
        h, t, _ = http([(r"cdn\.coverr\.co", head)] + ROUTES)
        r = FF.download_one(h, DB, "coverr:AAAA111111", self.out, self.opts(dry_run=True))
        self.assertTrue(r["dry_run"])
        self.assertEqual((r["width"], r["height"], r["bytes"], r["size_from"]), (1920, 1080, 12 * 1048576, "HEAD"))
        self.assertIn("1920x1080, 12.0 MB (HEAD)", FF._dry_text(r))
        self.assertFalse(any(p.is_file() for p in self.out.rglob("*")) if self.out.exists() else False)

    def test_sidecar_never_holds_a_key(self):
        key = "pbTESTKEY9876543210"
        rec = FF.make_result(DB, "pixabay", 5, title="x", page_url="https://pixabay.com/videos/x-5/",
                             file_url=f"https://cdn.pixabay.com/video/x.mp4?token={key}",
                             licence=FF.source_licence("pixabay", FF.sources_by_id(DB)["pixabay"]))
        self.results.write_text(json.dumps({"results": [rec]}), encoding="utf-8")
        h, _, _ = http([(r"cdn\.pixabay\.com", (200, MP4, {"Content-Type": "video/mp4"}))])
        with mock.patch.dict(os.environ, {"PIXABAY_API_KEY": key}), mock.patch.object(FF, "measure", return_value={}):
            r = FF.download_one(h, DB, "pixabay:5", self.out, self.opts())
        self.assertNotIn(key, FF.sidecar_for(self.out / r["file"]).read_text(encoding="utf-8"))


# ------------------------------------------------------------------------------------------------- probe, CLI

class ProbeAndCliTest(unittest.TestCase):
    def test_probe_statuses(self):
        def freepik(req):  # urllib follows the 301 silently and raises the 403 of the page it landed on
            raise urllib.error.HTTPError("https://www.freepik.com/videos", 403, "Forbidden", email.message.Message(),
                                         io.BytesIO(b""))
        routes = [(r"pexels\.com/search", (403, "")), (r"api\.pexels\.com", (401, "")),
                  (r"commons\.wikimedia\.org", "{}"), (r"upload\.wikimedia\.org", (429, "", {"Retry-After": "600"})),
                  (r"mixkit\.co", (206, MP4)), (r"videvo\.net", freepik), (r"videezy\.com", (403, "")),
                  (r"mazwai\.com", lambda req: Resp("https://www.freepik.com/videos", 200, b"<html>", {}))]
        h, _, _ = http(routes)
        rep = FF.run_probe(h, DB, ["pexels", "wikimedia", "mixkit", "videvo", "videezy", "mazwai"])
        st = {s["id"]: s for s in rep["sources"]}
        self.assertEqual(st["pexels"]["status"], "needs-key")
        self.assertEqual(st["wikimedia"]["status"], "partial")
        self.assertEqual(st["mixkit"]["status"], "ok")
        self.assertEqual(st["videezy"]["status"], "blocked")  # a 403 on its own domain is a block, not a move
        self.assertNotIn("final_url", st["videezy"]["probes"][0])
        for sid in ("videvo", "mazwai"):  # absorbed by another domain: "moved", whatever that domain answers
            self.assertEqual(st[sid]["status"], "moved", sid)
            self.assertEqual(st[sid]["probes"][0]["verdict"], "moved")
            self.assertEqual(st[sid]["probes"][0]["final_url"], "https://www.freepik.com/videos")
            self.assertFalse(st[sid]["changed"])  # the database already records the move
        self.assertEqual(st["videvo"]["probes"][0]["http"], 403)
        self.assertFalse(st["pexels"]["changed"])
        self.assertEqual(rep["schema"], FF.PROBE_SCHEMA)

    def test_a_same_site_redirect_is_not_a_move(self):
        h, _, _ = http([(r"archive\.org", lambda req: Resp("https://ia800100.us.archive.org/x", 200, b"{}", {}))])
        rep = FF.run_probe(h, DB, ["archive"])
        self.assertEqual(rep["sources"][0]["status"], "ok")
        self.assertEqual(rep["sources"][0]["probes"][0]["final_url"], "https://ia800100.us.archive.org/x")

    def test_probe_timeout(self):
        def boom(req, timeout):
            raise urllib.error.URLError("_ssl.c:1015: The handshake operation timed out")
        h = FF.Http(delay=0, transport=boom, sleep=lambda s: None)
        rep = FF.run_probe(h, DB, ["lifeofvids"])
        self.assertEqual(rep["sources"][0]["status"], "timeout")

    def test_cli_offline_commands(self):
        run = lambda *a: subprocess.run([sys.executable, str(SCRIPT), *a], capture_output=True, text=True, timeout=60)  # noqa: E731
        self.assertEqual(run("--help").returncode, 0)
        chk = run("check")
        self.assertEqual(chk.returncode, 0, chk.stderr)
        self.assertIn("17 sources", chk.stdout)
        rows = json.loads(run("sources", "--json", "--searchable").stdout)
        self.assertEqual({r["id"] for r in rows}, {"pexels", "pixabay", "mixkit", "coverr", "wikimedia", "archive", "nasa"})
        pin = json.loads(run("sources", "--id", "pinterest").stdout)
        self.assertFalse(pin["licence_source"])
        self.assertIn("dareful", run("sources", "--find", "4K").stdout)
        self.assertEqual(run("search", "sea", "--sources", "nosuchsite").returncode, 1)

    def test_cli_search_and_download_with_a_fake_network(self):
        with tempfile.TemporaryDirectory() as d:
            save, out = Path(d) / "r.json", Path(d) / "clips"
            fake = lambda args: FF.Http(delay=0, transport=Transport(  # noqa: E731
                [(r"cdn\.coverr\.co", (200, MP4, {"Content-Type": "video/mp4"}))] + ROUTES), sleep=lambda s: None)
            with mock.patch.object(FF, "make_http", fake), mock.patch.dict(os.environ, NO_KEYS), \
                    mock.patch.object(FF, "measure", return_value={}), mock.patch("sys.stdout", new_callable=io.StringIO) as so:
                self.assertEqual(FF.main(["search", "sea", "--sources", "coverr,wikimedia", "--save", str(save)]), 0)
                self.assertEqual(FF.main(["download", "coverr:BBBB222222", "--results", str(save), "--out", str(out)]), 0)
                self.assertEqual(FF.main(["credits", str(out)]), 0)
            self.assertIn("coverr:AAAA111111", so.getvalue())
            self.assertTrue((out / "coverr-BBBB222222.mp4").is_file())
            self.assertIn("Example Wave Shooter", (out / "ATTRIBUTION.md").read_text(encoding="utf-8"))
            data = json.loads(save.read_text(encoding="utf-8"))
            self.assertEqual(data["query"], "sea")

    def test_invalid_database_stops_every_command(self):
        with tempfile.TemporaryDirectory() as d:
            bad = Path(d) / "db.json"
            bad.write_text(json.dumps({"schema": "x", "sources": []}), encoding="utf-8")
            with mock.patch("sys.stderr", new_callable=io.StringIO) as se:
                self.assertEqual(FF.main(["--db", str(bad), "sources"]), 1)
            self.assertIn("invalid", se.getvalue())
            with mock.patch("sys.stdout", new_callable=io.StringIO):
                self.assertEqual(FF.main(["--db", str(bad), "check"]), 1)

    def test_paid_stock_is_not_listed_as_free(self):
        run = lambda *a: subprocess.run([sys.executable, str(SCRIPT), *a], capture_output=True, text=True, timeout=60)  # noqa: E731
        free = {r["id"] for r in json.loads(run("sources", "--commercial", "--no-attribution", "--json").stdout)}
        self.assertEqual(free, {"pexels", "pixabay", "coverr", "lifeofvids"})
        self.assertNotIn("storyblocks", {r["id"] for r in json.loads(run("sources", "--commercial", "--json").stdout)})
        paid = {r["id"] for r in json.loads(run("sources", "--commercial", "--include-paid", "--json").stdout)}
        self.assertIn("storyblocks", paid)
        self.assertIn("storyblocks", run("sources").stdout)  # the plain list still shows it, marked paid


# ------------------------------------------------------------------------------------------------- review fixes

NASA_SPACED = [(r"images-api\.nasa\.gov/search", fixture("nasa_search_spaced.json")),
               (r"images-api\.nasa\.gov/asset/", fixture("nasa_asset_spaced.json")),
               (r"metadata\.json$", fixture("nasa_metadata.json"))]
SPACED_ID = "Synthetic Pad Dust Removal"


class NasaSpacedIdTest(unittest.TestCase):
    """The NASA asset API returns links with raw spaces; http.client refuses them (InvalidURL, not a ValueError)."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.out = Path(self.tmp.name) / "clips"

    def tearDown(self):
        self.tmp.cleanup()

    def test_variant_links_are_percent_encoded_once(self):
        vids, meta = FF.nasa_variants(json.loads(fixture("nasa_asset_spaced.json")))
        enc = "Synthetic%20Pad%20Dust%20Removal"
        self.assertEqual(vids, [f"https://images-assets.nasa.gov/video/{enc}/{enc}~orig.mp4",
                                f"https://images-assets.nasa.gov/video/{enc}/{enc}~large.mp4"])
        self.assertEqual(meta, f"https://images-assets.nasa.gov/video/{enc}/metadata.json")
        self.assertEqual(FF.quote_path(vids[0]), vids[0])  # already encoded links are not encoded twice

    def test_filtered_search_with_spaced_ids_succeeds(self):
        h, t, _ = http(NASA_SPACED)
        rep = FF.run_search(h, DB, "launch", ["nasa"], 3, {"min_height": 1080})  # reads metadata.json too
        self.assertEqual(rep["sources"]["nasa"]["status"], "ok", rep["sources"]["nasa"])
        r = rep["results"][0]
        self.assertEqual((r["id"], r["height"]), (f"nasa:{SPACED_ID}", 2160))
        self.assertEqual(r["page_url"], "https://images.nasa.gov/details/Synthetic%20Pad%20Dust%20Removal")
        self.assertIn(r["page_url"], r["attribution"])
        self.assertFalse([u for u in t.urls() if " " in u])
        self.assertTrue(any(u.endswith("/metadata.json") for u in t.urls()))

    def test_download_of_a_spaced_id(self):
        h, t, _ = http([(r"~orig\.mp4$", (200, MP4, {"Content-Type": "video/mp4"}))] + NASA_SPACED)
        with mock.patch.object(FF, "measure", return_value={}):
            r = FF.download_one(h, DB, f"nasa:{SPACED_ID}", self.out,
                                {"results": self.out / "none.json", "max_mb": 50})
        self.assertEqual(r["file"], "nasa-Synthetic_Pad_Dust_Removal.mp4")
        side = json.loads(FF.sidecar_for(self.out / r["file"]).read_text(encoding="utf-8"))
        self.assertIn("Synthetic%20Pad%20Dust%20Removal~orig.mp4", side["result"]["file_url"])
        self.assertFalse([u for u in t.urls() if " " in u])

    def test_an_invalid_url_is_an_http_error_not_a_traceback(self):
        def strict(req, timeout):
            raise InvalidURL("URL can't contain control characters")
        h = FF.Http(delay=0, transport=strict, sleep=lambda s: None)
        with self.assertRaisesRegex(FF.HttpError, "InvalidURL"):
            h.get_json("https://images-assets.nasa.gov/video/a b/metadata.json")
        rep = FF.run_search(h, DB, "launch", ["nasa", "wikimedia"], 3, {})
        self.assertEqual({v["status"] for v in rep["sources"].values()}, {"error"})


class NetworkFailureTest(unittest.TestCase):
    """A read that times out, a reset or a cut-off body after the headers is a FootageError, never a traceback."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_a_stalled_read_on_one_source_keeps_the_search_and_its_save(self):
        save = self.dir / "last.json"
        stalled = lambda req: Failing(req.full_url, b"{}", {}, TimeoutError("The read operation timed out"))  # noqa: E731
        fake = lambda args: FF.Http(delay=0, transport=Transport(  # noqa: E731
            [(r"images-api\.nasa\.gov", stalled)] + ROUTES), sleep=lambda s: None)
        with mock.patch.object(FF, "make_http", fake), mock.patch.dict(os.environ, NO_KEYS), \
                mock.patch("sys.stdout", new_callable=io.StringIO):
            rc = FF.main(["search", "city", "--sources", "wikimedia,nasa,archive", "--delay", "0", "--save", str(save)])
        self.assertEqual(rc, 0)
        data = json.loads(save.read_text(encoding="utf-8"))
        self.assertEqual(data["sources"]["nasa"]["status"], "error")
        self.assertIn("transfer failed (TimeoutError)", data["sources"]["nasa"]["detail"])
        self.assertEqual(data["sources"]["wikimedia"]["status"], "ok")
        self.assertEqual(data["sources"]["archive"]["status"], "ok")

    def test_a_reset_mid_file_fails_one_target_and_the_batch_goes_on(self):
        h, _, _ = http(ROUTES)
        with mock.patch.dict(os.environ, NO_KEYS):
            rep = FF.run_search(h, DB, "sea", ["coverr"], 10, {})
        results = self.dir / "r.json"
        results.write_text(json.dumps(rep), encoding="utf-8")
        out = self.dir / "clips"
        reset = lambda req: Failing(req.full_url, MP4, {"Content-Type": "video/mp4"},  # noqa: E731
                                    ConnectionResetError(104, "Connection reset by peer"), good=64)
        cut = lambda req: Failing(req.full_url, MP4, {"Content-Type": "video/mp4"}, IncompleteRead(b"", 100), good=64)  # noqa: E731
        h, _, _ = http([(r"calm-waves-1111", reset), (r"waves-near-the-coast-2222", cut)])
        for rid, name in (("coverr:AAAA111111", "ConnectionResetError"), ("coverr:BBBB222222", "IncompleteRead")):
            with self.assertRaisesRegex(FF.FootageError, rf"transfer failed \({name}\)"):
                FF.download_one(h, DB, rid, out, {"results": results, "max_mb": 50})
        self.assertEqual(list(out.glob("*")), [])  # no .part file is left behind
        fake = lambda args: FF.Http(delay=0, transport=Transport(  # noqa: E731
            [(r"calm-waves-1111", reset), (r"cdn\.coverr\.co", (200, MP4, {"Content-Type": "video/mp4"}))]),
            sleep=lambda s: None)
        with mock.patch.object(FF, "make_http", fake), mock.patch.object(FF, "measure", return_value={}), \
                mock.patch("sys.stdout", new_callable=io.StringIO), mock.patch("sys.stderr", new_callable=io.StringIO) as se:
            rc = FF.main(["download", "coverr:AAAA111111", "coverr:BBBB222222", "--results", str(results), "--out", str(out)])
        self.assertEqual(rc, 1)
        self.assertIn("coverr:AAAA111111\tFAILED", se.getvalue())
        self.assertTrue((out / "coverr-BBBB222222.mp4").is_file())  # the second target still downloaded

    def test_pexels_endpoint_that_does_not_answer(self):
        sf = FF._sibling("stock_fetch")
        with mock.patch.dict(os.environ, NO_KEYS), \
                mock.patch.object(sf, "resolve_pexels", side_effect=urllib.error.URLError(TimeoutError("timed out"))), \
                mock.patch("sys.stderr", new_callable=io.StringIO) as se:
            rc = FF.main(["download", "https://www.pexels.com/video/video-of-forest-1448735/", "--out", str(self.dir)])
        self.assertEqual(rc, 1)
        self.assertIn("pexels 1448735: the download endpoint did not answer (TimeoutError)", se.getvalue())

    def test_run_search_backstop_for_unworded_network_errors(self):
        h, _, _ = http(ROUTES)
        with mock.patch.dict(FF.SEARCHERS, {"coverr": mock.Mock(side_effect=ConnectionResetError(104, "reset"))}):
            rep = FF.run_search(h, DB, "sea", ["coverr", "wikimedia"], 3, {})
        self.assertEqual(rep["sources"]["coverr"], {"status": "error", "detail": "network failure (ConnectionResetError)"})
        self.assertEqual(rep["sources"]["wikimedia"]["status"], "ok")


class RetiredLicenceTest(unittest.TestCase):
    """Sampling, Sampling+, Developing Nations (and the CC-GPL/LGPL wrappers) are not BY-family licences."""
    CASES = {
        "http://creativecommons.org/licenses/sampling+/1.0/": "CC Sampling+ 1.0",
        "https://creativecommons.org/licenses/sampling/1.0/": "CC Sampling 1.0",
        "http://creativecommons.org/licenses/nc-sampling+/1.0/": "CC NonCommercial Sampling+ 1.0",
        "http://creativecommons.org/licenses/devnations/2.0/": "CC Developing Nations 2.0",
        "http://creativecommons.org/licenses/GPL/2.0/": "CC GNU GPL 2.0",
        "http://creativecommons.org/licenses/LGPL/2.1/": "CC GNU LGPL 2.1",
        "http://creativecommons.org/licenses/nc/1.0/": "CC nc 1.0",
    }

    def test_they_are_unverified_credit_required_and_fail_commercial(self):
        for url, name in self.CASES.items():
            with self.subTest(url=url):
                lic = FF.classify_licence(None, url)
                self.assertEqual(lic["name"], name)
                self.assertFalse(lic["verified"])
                self.assertIs(lic["attribution_required"], True)
                self.assertIsNone(lic["commercial"])
                self.assertIsNone(lic["derivatives"])
                self.assertIn("read the deed", lic["note"])
                rec = {"licence": lic, "flags": []}
                self.assertIsNotNone(FF.keep(rec, {"commercial": True}))
                self.assertIsNone(FF.keep(rec, {}))  # kept without --commercial, flagged "commercial ?"

    def test_the_by_family_is_unchanged(self):
        lic = FF.classify_licence(None, "http://creativecommons.org/licenses/by-nc-sa/3.0/")
        self.assertEqual((lic["name"], lic["verified"], lic["commercial"]), ("CC BY-NC-SA 3.0", True, False))

    def test_an_archive_item_under_sampling_plus(self):
        meta = json.loads(fixture("archive_meta.json"))
        meta["metadata"]["licenseurl"] = "http://creativecommons.org/licenses/sampling+/1.0/"
        r = FF.archive_result(DB, {"identifier": "NYC"}, meta)
        self.assertEqual(r["licence"]["name"], "CC Sampling+ 1.0")
        self.assertIsNotNone(FF.keep(r, {"commercial": True}))
        with tempfile.TemporaryDirectory() as d:
            Path(d, "x.mp4.json").write_text(json.dumps({"schema": FF.ASSET_SCHEMA, "file": "x.mp4", "result": r,
                                                         "licence": r["licence"], "attribution": r["attribution"]}),
                                             encoding="utf-8")
            text = FF.credits_markdown(Path(d))
        self.assertIn("| CC Sampling+ 1.0 | yes | check |", text)
        self.assertNotIn("*(optional)*", text)


class MixkitSizesTest(unittest.TestCase):
    """Free clips serve -1080 (often -2160) to scripts; Restricted clips only -720 (measured 2026-10-29)."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.out = self.dir / "clips"
        h, _, _ = http(ROUTES)
        rep = FF.run_search(h, DB, "sea", ["mixkit"], 10, {})  # licences not read yet: both clips at -720
        self.assertEqual({r["file_url"].rsplit("-", 1)[-1] for r in rep["results"]}, {"720.mp4"})
        self.results = self.dir / "r.json"
        self.results.write_text(json.dumps(rep), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def get(self, rid, files):
        h, t, _ = http(files + ROUTES)
        with mock.patch.object(FF, "measure", return_value={}):
            r = FF.download_one(h, DB, rid, self.out, {"results": self.results, "max_mb": 50})
        side = json.loads(FF.sidecar_for(self.out / r["file"]).read_text(encoding="utf-8"))
        return side["result"], [u for u in t.urls() if "assets.mixkit.co" in u]

    def test_a_free_clip_without_a_4k_file_comes_at_1080p(self):
        ok = (200, MP4, {"Content-Type": "video/mp4"})
        rec, tried = self.get("mixkit:40002", [(r"-2160\.mp4", (403, "<Error/>", {"Content-Type": "application/xml"})),
                                                (r"-1080\.mp4", ok)])
        self.assertEqual([u.rsplit("/", 1)[-1] for u in tried], ["40002-2160.mp4", "40002-1080.mp4"])
        self.assertEqual((rec["file_url"].rsplit("/", 1)[-1], rec["quality"]), ("40002-1080.mp4", 1080))
        self.assertEqual((rec["width"], rec["height"]), (1920, 1080))
        self.assertNotIn("smaller-variant", rec["flags"])  # 1080p is what a Free clip is expected to have
        self.assertEqual(rec["licence"]["name"], FF.MIXKIT_FREE)

    def test_a_free_clip_with_a_4k_file(self):
        rec, tried = self.get("mixkit:40002", [(r"-2160\.mp4", (206, MP4, {"Content-Type": "video/mp4"}))])
        self.assertEqual(len(tried), 1)
        self.assertEqual((rec["quality"], rec["width"], rec["height"]), (2160, 3840, 2160))

    def test_a_free_clip_falls_back_to_720p_and_says_so(self):
        no = (403, "<Error/>", {"Content-Type": "application/xml"})
        rec, tried = self.get("mixkit:40002", [(r"-2160\.mp4|-1080\.mp4", no),
                                                (r"-720\.mp4", (200, MP4, {"Content-Type": "video/mp4"}))])
        self.assertEqual(len(tried), 3)
        self.assertEqual(rec["quality"], 720)
        self.assertIn("smaller-variant", rec["flags"])

    def test_a_restricted_clip_never_asks_for_more_than_720p(self):
        rec, tried = self.get("mixkit:40001", [(r"-720\.mp4", (200, MP4, {"Content-Type": "video/mp4"}))])
        self.assertEqual([u.rsplit("/", 1)[-1] for u in tried], ["40001-720.mp4"])
        self.assertEqual(rec["licence"]["name"], FF.MIXKIT_RESTRICTED)

    def test_a_bare_id_reads_the_licence_through_the_slug_redirect(self):
        # /free-stock-video/<id>/ redirects to a search page; any "<slug>-<id>/" redirects to the clip page
        canon = "https://mixkit.co/free-stock-video/synthetic-traffic-from-above-40002/"
        page = fixture("mixkit_clip_free.html").replace("<head>", f'<head><link rel="canonical" href="{canon}" />')
        h, t, _ = http([(r"free-stock-video/clip-40002/$", page), (r"-1080\.mp4", (200, MP4, {"Content-Type": "video/mp4"})),
                        (r"-2160\.mp4", (403, "<Error/>"))])
        with mock.patch.object(FF, "measure", return_value={}):
            r = FF.download_one(h, DB, "mixkit:40002", self.out, {"results": self.dir / "none.json", "max_mb": 50})
        side = json.loads(FF.sidecar_for(self.out / r["file"]).read_text(encoding="utf-8"))
        self.assertEqual(t.urls()[0], "https://mixkit.co/free-stock-video/clip-40002/")
        self.assertEqual(side["licence"]["name"], FF.MIXKIT_FREE)
        self.assertEqual(side["result"]["page_url"], canon)
        self.assertIn(canon, side["attribution"])
        self.assertTrue(side["result"]["file_url"].endswith("40002-1080.mp4"))

    def test_a_hand_made_mixkit_record_keeps_its_own_file(self):
        rec = FF.manual_record(DB, "https://mixkit.co/some/odd/link.mp4",
                               {"licence": "Mixkit Stock Video Free License", "licence_url": "https://mixkit.co/license/"})
        self.assertEqual(rec["source"], "mixkit")
        before = rec["file_url"]
        rec["licence"] = {"name": FF.MIXKIT_FREE}
        self.assertEqual(FF.mixkit_apply_files(rec)["file_url"], before)
        self.assertNotIn("alternates", rec)

    def test_min_height_reads_the_licence_of_clips_that_would_pass_at_1080p(self):
        h, t, _ = http(ROUTES)
        rep = FF.run_search(h, DB, "sea", ["mixkit"], 10, {"min_height": 1080})
        self.assertEqual([u for u in t.urls() if "free-stock-video/synthetic" in u],
                         ["https://mixkit.co/free-stock-video/synthetic-traffic-from-above-40002/"])  # 40001 passes at 720p
        got = {r["id"]: (r["width"], r["height"]) for r in rep["results"]}
        self.assertEqual(got, {"mixkit:40001": (720, 1280), "mixkit:40002": (1920, 1080)})
        h, t, _ = http(ROUTES)
        rep = FF.run_search(h, DB, "sea", ["mixkit"], 10, {"min_height": 1900, "orientation": "portrait"})
        self.assertEqual([u for u in t.urls() if "free-stock-video/synthetic" in u],
                         ["https://mixkit.co/free-stock-video/synthetic-night-walk-in-a-big-city-40001/"])
        self.assertEqual(rep["results"], [])  # Restricted: 720x1280 only, under 1900
        self.assertEqual(rep["sources"]["mixkit"]["dropped"], {"height 1280 < 1900": 1, "height 720 < 1900": 1})


# ------------------------------------------------------------------------------------------------- field report fixes
# Bugs hit live on 2026-10-29 by a footage scout downloading 17 licensed clips (each test names the symptom).

OK_MP4 = (200, MP4, {"Content-Type": "video/mp4"})
NO_FILE = (403, "<Error/>", {"Content-Type": "application/xml"})
CHALLENGE = fixture("cloudflare_challenge.html")
HASHES = {"2160p": "synthhash2160aaaaaaaaaaaaaa", "1080p": "synthhash1080bbbbbbbbbbbbbb",
          "720p": "synthhash0720cccccccccccccc"}


def modal(req):
    """The small page a Mixkit download route answers, naming the hashed file of that size."""
    t = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(req.full_url).query)).get("type", "720p")
    cid = re.search(r"/download/(\d+)/", req.full_url).group(1)
    return fixture("mixkit_download_modal.html").replace("{hash}", HASHES[t]).replace("{id}", cid).replace("{type}", t)


NEW_ROUTES = [
    (r"mixkit\.co/free-stock-video/download/", modal),
    (r"free-stock-video/(clip-50001|synthetic-droplet-on-a-leaf-50001)/$", fixture("mixkit_clip_hashed.html")),
    (r"free-stock-video/(clip-50002|synthetic-misty-hills-50002)/$", fixture("mixkit_clip_active_storage.html")),
    (r"free-stock-video/clip-50003/$", fixture("mixkit_clip_restricted_button.html")),
    (r"synthetic-woman-sending-messages-on-a-phone-50004/$", fixture("mixkit_clip_free.html")),
    (r"mixkit\.co/free-stock-video/discover/", fixture("mixkit_discover_new.html")),
    (r"assets\.mixkit\.co/videos/5000\d/", NO_FILE),  # newer clips have no <id>-<q>.mp4 file
]


def mixkit_get(case, rid, extra=(), **opts):
    """download_one of a Mixkit id with no results file; returns (result, sidecar or None, transport)."""
    h, t, _ = http(list(extra) + NEW_ROUTES)
    with mock.patch.object(FF, "measure", return_value={}):
        r = FF.download_one(h, DB, rid, case.out, {"results": case.dir / "none.json", "max_mb": 300, **opts})
    side = None if r.get("dry_run") else json.loads(FF.sidecar_for(case.out / r["file"]).read_text(encoding="utf-8"))
    return r, side, t


class TempDirCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.out = self.dir / "clips"

    def tearDown(self):
        self.tmp.cleanup()


class MixkitNewClipsTest(TempDirCase):
    """`download mixkit:100896` failed with HTTP 403 from .../100896-720.mp4: newer clips use hashed file links
    (assets.mixkit.co/<hash>) or .../active_storage/video_items/<id>/<ts>/<id>-video-<q>.mp4, offered by the clip
    page's download options."""

    def test_page_download_options(self):
        vs = FF.mixkit_page_variants(fixture("mixkit_clip_hashed.html"), 50001)
        self.assertEqual([v["quality"] for v in vs], [2160, 1080, 720])
        self.assertEqual([v["label"] for v in vs], ["4K", "Full HD", "HD Ready"])
        self.assertEqual([v["mb"] for v in vs], [58.21, 44.59, 4.03])
        self.assertEqual(vs[0]["bytes"], round(58.21 * 1048576))
        # the listed 4096x2160 and 1920x1080 are kept; the site's "1080x720" for the 720p file is scaled instead
        self.assertEqual([(v["width"], v["height"]) for v in vs], [(4096, 2160), (1920, 1080), (1280, 720)])
        self.assertEqual(vs[1]["route"], "https://mixkit.co/free-stock-video/download/50001/?context=sidebar&type=1080p")
        btn = FF.mixkit_page_variants(fixture("mixkit_clip_restricted_button.html"), 50003)
        self.assertEqual([(v["quality"], v["route"]) for v in btn],
                         [(720, "https://mixkit.co/free-stock-video/download/50003/?context=sidebar")])
        self.assertEqual(FF.mixkit_page_variants(fixture("mixkit_clip_free.html"), 40002), [])
        self.assertEqual(FF.mixkit_pattern(50001, "https://assets.mixkit.co/synthcontentbbbbbbbbbbbbbb"), ("hashed", None))
        base = "https://assets.mixkit.co/active_storage/video_items/50002/1721168872/50002-video"
        self.assertEqual(FF.mixkit_pattern(50002, base + "-720.mp4"), ("active_storage", base))
        self.assertEqual(FF.mixkit_pattern(15209, "https://assets.mixkit.co/videos/15209/15209-720.mp4"), ("legacy", None))
        self.assertEqual(FF.mixkit_file(50002, 1080, "active_storage", base), base + "-1080.mp4")
        self.assertIsNone(FF.mixkit_file(50001, 1080, "hashed"))

    def test_a_hashed_clip_downloads_through_its_download_route(self):
        r, side, t = mixkit_get(self, "mixkit:50001", [(r"assets\.mixkit\.co/synthhash2160", OK_MP4)])
        self.assertEqual(t.urls(), ["https://mixkit.co/free-stock-video/clip-50001/",
                                    "https://mixkit.co/free-stock-video/download/50001/?context=sidebar&type=2160p",
                                    "https://assets.mixkit.co/synthhash2160aaaaaaaaaaaaaa"])  # the template is never tried
        res = side["result"]
        self.assertEqual(res["file_url"], "https://assets.mixkit.co/synthhash2160aaaaaaaaaaaaaa")
        self.assertEqual((res["quality"], res["width"], res["height"]), (2160, 4096, 2160))
        self.assertTrue(res["native"]["download_route"].endswith("type=2160p"))
        self.assertEqual(side["licence"]["name"], FF.MIXKIT_FREE)
        self.assertEqual(res["page_url"], "https://mixkit.co/free-stock-video/synthetic-droplet-on-a-leaf-50001/")
        self.assertEqual(res["thumb_url"], "https://assets.mixkit.co/synththumbaaaaaaaaaaaaaaaa1")
        self.assertEqual(res["preview_url"], "https://assets.mixkit.co/synthembedcccccccccccccccccc")
        self.assertNotIn("smaller-variant", res["flags"])
        self.assertEqual(r["quality"], 2160)

    def test_quality_cap_and_budget_use_the_listed_sizes(self):
        _, side, t = mixkit_get(self, "mixkit:50001", [(r"synthhash1080", OK_MP4)], max_quality=1080)
        self.assertFalse([u for u in t.urls() if "2160" in u])
        self.assertEqual((side["result"]["quality"], side["result"]["width"]), (1080, 1920))
        self.assertNotIn("smaller-variant", side["result"]["flags"])  # the size the user asked for
        shutil.rmtree(self.out)
        _, side, t = mixkit_get(self, "mixkit:50001", [(r"synthhash1080", OK_MP4)], max_mb=50)
        self.assertFalse([u for u in t.urls() if "2160" in u])  # 58.21 MB > 50: skipped without a request
        self.assertIn("smaller-variant", side["result"]["flags"])
        with self.assertRaisesRegex(FF.FootageError, r"every size is over --max-mb 3 \(the smallest is 4.0 MB\)"):
            mixkit_get(self, "mixkit:50001", max_mb=3)
        with self.assertRaisesRegex(FF.FootageError, "no file within --quality 480; it comes at 2160p 4096x2160"):
            mixkit_get(self, "mixkit:50001", max_quality=480)
        shutil.rmtree(self.out)
        _, side, _ = mixkit_get(self, "mixkit:50001", [(r"synthhash0720", OK_MP4)], max_height=1000)
        self.assertEqual((side["result"]["quality"], side["result"]["height"]), (720, 720))

    def test_dry_run_prints_the_listed_size_without_fetching(self):
        r, _, t = mixkit_get(self, "mixkit:50001", dry_run=True)
        self.assertEqual(t.urls(), ["https://mixkit.co/free-stock-video/clip-50001/"])  # the page only
        self.assertEqual((r["quality"], r["width"], r["height"], r["bytes"]), (2160, 4096, 2160, round(58.21 * 1048576)))
        self.assertEqual(FF._dry_text(r), "dry run: 2160p 4096x2160, 58.2 MB (listed by the source)")
        self.assertFalse(r["over_max_mb"])

    def test_active_storage_files_are_named_from_the_page(self):
        _, side, t = mixkit_get(self, "mixkit:50002", [(r"active_storage/.*50002-video-1080\.mp4$", OK_MP4)])
        self.assertEqual([u for u in t.urls() if "assets.mixkit.co" in u],
                         ["https://assets.mixkit.co/active_storage/video_items/50002/1721168872/50002-video-1080.mp4"])
        self.assertFalse([u for u in t.urls() if "/download/" in u])  # a direct file: no route needed
        self.assertEqual((side["result"]["quality"], side["result"]["width"], side["result"]["height"]), (1080, 1920, 1080))

    def test_a_template_that_answers_403_falls_back_to_the_route(self):
        page = fixture("mixkit_clip_hashed.html").replace("https://assets.mixkit.co/synthcontentbbbbbbbbbbbbbb",
                                                           "https://assets.mixkit.co/videos/50001/50001-720.mp4")
        _, side, t = mixkit_get(self, "mixkit:50001", [(r"free-stock-video/clip-50001/$", page),
                                                        (r"synthhash2160", OK_MP4)])
        self.assertEqual(t.urls()[1:], ["https://assets.mixkit.co/videos/50001/50001-2160.mp4",  # 403
                                        "https://mixkit.co/free-stock-video/download/50001/?context=sidebar&type=2160p",
                                        "https://assets.mixkit.co/synthhash2160aaaaaaaaaaaaaa"])
        self.assertEqual(side["result"]["quality"], 2160)

    def test_a_restricted_clip_with_one_button_stays_at_720p(self):
        _, side, t = mixkit_get(self, "mixkit:50003", [(r"/videos/50003/50003-720\.mp4$", OK_MP4)])
        self.assertEqual([u for u in t.urls() if "assets.mixkit.co" in u], ["https://assets.mixkit.co/videos/50003/50003-720.mp4"])
        self.assertEqual((side["licence"]["name"], side["result"]["quality"]), (FF.MIXKIT_RESTRICTED, 720))

    def test_a_hashed_clip_whose_page_fails_says_why(self):
        routes = [(r"free-stock-video/clip-50001/$", (500, "down"))]
        with self.assertRaisesRegex(FF.FootageError, "newer Mixkit clips have no <id>-<size>.mp4 file .* could not be read"):
            mixkit_get(self, "mixkit:50001", routes)

    def test_search_resolve_reads_licence_size_and_previews(self):
        h, t, _ = http(NEW_ROUTES)
        plain = FF.run_search(h, DB, "leaf", ["mixkit"], 10, {})
        r = {x["id"]: x for x in plain["results"]}
        self.assertFalse(r["mixkit:50001"]["licence"]["verified"])
        self.assertIn("size-from-thumbnail", r["mixkit:50001"]["flags"])
        self.assertEqual(r["mixkit:50001"]["thumb_url"], "https://assets.mixkit.co/synththumbaaaaaaaaaaaaaaaa1")
        self.assertEqual(r["mixkit:50002"]["preview_url"],
                         "https://assets.mixkit.co/active_storage/video_items/50002/1721168872/50002-video-360.mp4")
        self.assertEqual(r["mixkit:50002"]["file_url"],  # named from the card, not the <id>-720.mp4 template
                         "https://assets.mixkit.co/active_storage/video_items/50002/1721168872/50002-video-720.mp4")
        self.assertFalse([u for u in t.urls() if "free-stock-video/synthetic" in u or "clip-" in u])
        with mock.patch("sys.stdout", new_callable=io.StringIO) as so:
            FF.print_results(plain)
        self.assertIn("~1280x720", so.getvalue())
        self.assertIn("--resolve reads each clip page", so.getvalue())
        h, t, _ = http(NEW_ROUTES)
        rep = FF.run_search(h, DB, "leaf", ["mixkit"], 10, {"resolve": True})
        r = {x["id"]: x for x in rep["results"]}
        self.assertTrue(all(x["licence"]["verified"] for x in r.values()))
        self.assertEqual((r["mixkit:50001"]["width"], r["mixkit:50001"]["height"], r["mixkit:50001"]["quality"]),
                         (4096, 2160, 2160))
        self.assertNotIn("size-from-thumbnail", r["mixkit:50001"]["flags"])
        self.assertEqual(r["mixkit:50001"]["bytes"], round(58.21 * 1048576))
        self.assertEqual(len([u for u in t.urls() if "free-stock-video/synthetic" in u]), 3)
        self.assertEqual(rep["filters"], {"resolve": True})
        h, t, _ = http(NEW_ROUTES)
        FF.run_search(h, DB, "leaf", ["mixkit"], 1, {"resolve": True})
        self.assertEqual(len([u for u in t.urls() if "free-stock-video/synthetic" in u]), 1)  # stops once 1 is kept

    def test_match_and_no_people(self):
        h, _, _ = http(NEW_ROUTES)
        rep = FF.run_search(h, DB, "leaf", ["mixkit"], 10, {"match": "any", "no_people": True})
        self.assertEqual([r["id"] for r in rep["results"]], ["mixkit:50001"])
        self.assertEqual(rep["results"][0]["relevance"], 1.0)
        self.assertEqual(rep["sources"]["mixkit"]["dropped"], {"title matches no query word (--match any)": 1,
                                                               "people named in the title (--no-people)": 1})


class RelevanceTest(unittest.TestCase):
    """`search "seedling" --sources mixkit` returned 'Woman sending messages on Whatsapp' and 'Two cars speeding'."""

    def test_title_relevance(self):
        rel = lambda title, q, **kw: FF.relevance({"title": title, **kw}, q)  # noqa: E731
        self.assertEqual(rel("Woman sending messages on Whatsapp", "seedling"), 0)
        self.assertEqual(rel("Two cars speeding", "seedling"), 0)
        self.assertEqual(rel("Seedlings growing in soil", "seedling"), 1.0)
        self.assertEqual(rel("Cloud time-lapse over hills", "cloud timelapse"), 1.0)
        self.assertEqual(rel("Timelapse of clouds", "time lapse clouds"), 1.0)
        self.assertEqual(rel("Red sunset over the ocean", "sun rays clouds"), 0)
        self.assertEqual(rel("Rain on a window", "heavy rain"), 0.5)
        self.assertEqual(rel("Orbit", "aurora", native={"keywords": ["Aurora", "ISS"]}), 1.0)
        self.assertEqual(FF.query_terms("the video of rain"), ["rain"])
        self.assertIsNone(rel("x", ""))
        rec = {"title": "Rain on a window", "licence": {}, "flags": []}
        self.assertIsNone(FF.keep(rec, {"match": "any", "query": "heavy rain"}))
        self.assertEqual(FF.keep(rec, {"match": "all", "query": "heavy rain"}), "title misses a query word (--match all)")

    def test_people_words(self):
        self.assertEqual(FF.people_word({"title": "Couple walking on the beach"}), "couple")
        self.assertEqual(FF.people_word({"title": "Hands planting a seedling"}), "hands")
        self.assertEqual(FF.people_word({"title": "Scary woman seeing through the window"}), "woman")
        self.assertIsNone(FF.people_word({"title": "Leaf in the rain"}))
        self.assertIsNone(FF.people_word({"title": "Manta ray"}))  # whole words only


class ChallengeTest(TempDirCase):
    """The Mixkit download route sometimes answered a Cloudflare 'Just a moment...' page (HTML 200) that cleared
    about 3 minutes later. It is reported, never worked around."""

    def test_detects_the_interstitial(self):
        self.assertTrue(FF.is_challenge_page(CHALLENGE.encode()))
        self.assertTrue(FF.is_challenge_page(b"<html><head><title>Just a moment...</title></head></html>"))
        self.assertFalse(FF.is_challenge_page(fixture("mixkit_clip_hashed.html").encode()))
        self.assertFalse(FF.is_challenge_page(b""))
        self.assertTrue(FF.is_challenge_page(b"<script src=\"/cdn-cgi/challenge-platform/h/b/orchestrate/chl_page/v1"
                                             b"?ray=0000\"></script>"))

    def test_an_ordinary_page_with_cloudflares_bot_script_is_not_a_check(self):
        """Cloudflare injects a detection script into normal pages (seen on a Videezy clip page); a short page
        carrying it is not a "Just a moment..." check, and its host must not be blocked for the run."""
        for script in (b"/cdn-cgi/challenge-platform/scripts/precursor/main.js", b"/cdn-cgi/challenge-platform/scripts/jsd/main.js"):
            page = (b"<html><head><title>Ocean waves in slow motion - Free HD Video Clips</title></head><body>"
                    b"<video src=\"https://cdn.example.org/ocean.mp4\"></video><script>(function(){var s=document."
                    b"createElement('script');s.src='" + script + b"';document.body.appendChild(s);})();</script>"
                    b"</body></html>")
            self.assertFalse(FF.is_challenge_page(page), script)
            h, _, _ = http([(r"example\.org", (200, page))])
            self.assertIn(b"ocean.mp4", h.get_bytes("https://www.example.org/clip/1"))
            self.assertEqual(h.challenged, set())

    def test_a_challenged_route_is_reported_and_the_host_left_alone(self):
        t = Transport([(r"mixkit\.co/free-stock-video/download/", CHALLENGE)] + NEW_ROUTES)
        fake = lambda args: FF.Http(delay=0, transport=t, sleep=lambda s: None)  # noqa: E731
        with mock.patch.object(FF, "make_http", fake), mock.patch.object(FF, "measure", return_value={}), \
                mock.patch("sys.stdout", new_callable=io.StringIO), mock.patch("sys.stderr", new_callable=io.StringIO) as se:
            rc = FF.main(["download", "mixkit:50001", "mixkit:50002", "--out", str(self.out),
                          "--results", str(self.dir / "none.json")])
        self.assertEqual(rc, 1)
        err = se.getvalue()
        self.assertIn('mixkit.co answered with a Cloudflare "Just a moment..." browser check', err)
        self.assertIn("does not try to get past it", err)
        self.assertIn("mixkit:50002\tFAILED", err)
        self.assertIn("earlier in this run", err)
        self.assertIn("2 target(s) not fetched: mixkit.co answered with a Cloudflare browser check", err)
        self.assertEqual([u for u in t.urls() if urllib.parse.urlsplit(u).hostname == "mixkit.co"],
                         ["https://mixkit.co/free-stock-video/clip-50001/",
                          "https://mixkit.co/free-stock-video/download/50001/?context=sidebar&type=2160p"])
        self.assertFalse(list(self.out.glob("*.mp4")) if self.out.exists() else [])

    def test_retry_challenge_waits_once_then_asks_again(self):
        answers = iter([CHALLENGE])
        route = lambda req: next(answers, None) or modal(req)  # noqa: E731
        sleeps = []
        h = FF.Http(delay=0, transport=Transport([(r"/download/", route)]), sleep=sleeps.append, challenge_wait=180)
        url = FF.mixkit_follow_route(h, "https://mixkit.co/free-stock-video/download/50001/?context=sidebar&type=1080p")
        self.assertEqual(url, "https://assets.mixkit.co/synthhash1080bbbbbbbbbbbbbb")
        self.assertEqual(sleeps, [180.0])
        sleeps2 = []
        h2 = FF.Http(delay=0, transport=Transport([(r".", CHALLENGE)]), sleep=sleeps2.append, challenge_wait=180)
        with self.assertRaises(FF.ChallengeError):
            h2.get_text("https://mixkit.co/free-stock-video/download/1/?type=720p")
        with self.assertRaisesRegex(FF.ChallengeError, "earlier in this run"):
            h2.get_text("https://mixkit.co/free-stock-video/clip-1/")
        self.assertEqual(sleeps2, [180.0])  # waited once, then left the host alone
        self.assertEqual(FF.Http(challenge_wait=5000).challenge_wait, FF.MAX_CHALLENGE_WAIT)

    def test_header_challenge_search_and_probe(self):
        hdr = (403, "<html></html>", {"cf-mitigated": "challenge"})
        h, t, sleeps = http([(r"mixkit\.co", hdr)])
        rep = FF.run_search(h, DB, "sea", ["mixkit"], 5, {})
        st = rep["sources"]["mixkit"]
        self.assertEqual((st["status"], st["challenge"]), ("error", True))
        self.assertIn("browser check", st["detail"])
        self.assertEqual((len(t.calls), sleeps), (1, []))  # no retry
        h, _, _ = http([(r"mixkit\.co/free-stock-video/discover/", CHALLENGE)])
        st = FF.run_search(h, DB, "sea", ["mixkit"], 5, {})["sources"]["mixkit"]
        self.assertTrue(st["challenge"])
        h, _, _ = http([(r"mixkit\.co", hdr)])
        p = FF.run_probe(h, DB, ["mixkit"])["sources"][0]
        self.assertEqual(p["status"], "blocked")
        self.assertTrue(p["probes"][0]["challenge"])

    def test_a_challenge_served_instead_of_a_file(self):
        h, _, _ = http([(r"cdn\.example\.org", (200, CHALLENGE, {"Content-Type": "text/html"}))])
        with self.assertRaises(FF.ChallengeError):
            FF.fetch_file(h, "https://cdn.example.org/a.mp4", self.dir / "a.mp4", 10)
        self.assertIn("cdn.example.org", h.challenged)
        self.assertFalse(list(self.dir.glob("a.mp4*")))


class RateLimitTest(TempDirCase):
    """`search "rain"` printed a bare `# wikimedia error HTTP 429` (Retry-After 46 > 30), and the other sources'
    results had to be found again."""

    def cli(self, routes, *argv):
        t, sleeps, real = Transport(routes), [], FF.make_http

        def fake(args):
            h = real(args)
            h.transport, h.sleep = t, sleeps.append
            return h
        with mock.patch.object(FF, "make_http", fake), mock.patch.dict(os.environ, NO_KEYS), \
                mock.patch("sys.stdout", new_callable=io.StringIO) as so:
            rc = FF.main(list(argv))
        return rc, so.getvalue(), t, sleeps

    def test_search_summary_names_the_retry_after_and_keeps_the_rest(self):
        save = self.dir / "r.json"
        routes = [(r"commons\.wikimedia\.org", (429, "slow", {"Retry-After": "46"}))] + ROUTES
        rc, out, _, sleeps = self.cli(routes, "search", "sea", "--sources", "wikimedia,coverr", "--delay", "0",
                                      "--save", str(save))
        self.assertEqual(rc, 0)
        self.assertIn("Retry-After 46s is too long for --wait-429 30 (rerun with --wait-429 46", out)
        data = json.loads(save.read_text(encoding="utf-8"))
        self.assertEqual(data["sources"]["wikimedia"]["retry_after"], 46.0)
        self.assertTrue(any(r["source"] == "coverr" for r in data["results"]))
        self.assertEqual(sleeps, [])
        answers = iter([(429, "slow", {"Retry-After": "46"})])
        wiki = lambda req: next(answers, None) or (200, fixture("wikimedia_search.json"))  # noqa: E731
        rc, out, _, sleeps = self.cli([(r"commons\.wikimedia\.org", wiki)] + ROUTES, "search", "sea", "--sources",
                                      "wikimedia", "--delay", "0", "--wait-429", "60", "--save", str(save))
        self.assertIn(46.0, sleeps)
        self.assertEqual(json.loads(save.read_text(encoding="utf-8"))["sources"]["wikimedia"]["status"], "ok")

    def test_the_summary_hint_after_one_wait(self):
        h, _, sleeps = http([(r".", (429, "no", {"Retry-After": "3"}))])
        with self.assertRaises(FF.HttpError) as cm:
            h.get_json("https://commons.wikimedia.org/w/api.php?x=1")
        self.assertIn("rate limited; Retry-After 3s (again after one wait)", str(cm.exception))
        self.assertEqual((cm.exception.retry_after, sleeps), (3.0, [3.0]))
        rep = {"sources": {"wikimedia": {"status": "error", "detail": str(cm.exception), "retry_after": 3.0}}, "results": []}
        with mock.patch("sys.stdout", new_callable=io.StringIO) as so:
            FF.print_results(rep)
        self.assertIn("[Retry-After 3s: --wait-429 3 waits for it (at most 900), or search again later with "
                      "--retry-failed]", so.getvalue())
        h, _, _ = http([(r".", (429, "no", {"Retry-After": "3600"}))])
        with self.assertRaisesRegex(FF.HttpError, r"longer than --wait-429 can wait \(900 s\): try later"):
            h.get_json("https://upload.wikimedia.org/x.webm")
        h, _, sleeps = http([(r".", (429, "no"))])  # no Retry-After and --wait-429 0: one short wait, then the error
        h.max_retry_after = 0
        with self.assertRaisesRegex(FF.HttpError, r"HTTP 429 .*: rate limited \(again after one wait\)$"):
            h.get_json("https://commons.wikimedia.org/w/api.php")
        self.assertEqual(sleeps, [2.0])

    def test_wait_429_is_bounded(self):
        with mock.patch("sys.stderr", new_callable=io.StringIO) as se, self.assertRaises(SystemExit) as cm:
            FF.build_parser().parse_args(["search", "x", "--wait-429", "1000"])
        self.assertEqual(cm.exception.code, 2)
        self.assertIn("between 0 and 900 seconds", se.getvalue())
        self.assertEqual(FF.Http(max_retry_after=5000).max_retry_after, FF.MAX_WAIT_429)

    def test_retry_after_as_a_date(self):
        when = email.utils.format_datetime(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=120))
        self.assertTrue(100 <= FF._seconds(when) <= 121)
        self.assertEqual(FF._seconds("7"), 7.0)
        self.assertIsNone(FF._seconds("soon"))

    def test_retry_failed_asks_only_the_sources_that_failed(self):
        save = self.dir / "r.json"
        self.cli([(r"commons\.wikimedia\.org", (429, "slow", {"Retry-After": "600"}))] + ROUTES,
                 "search", "sea", "--sources", "wikimedia,coverr", "--delay", "0", "--save", str(save))
        rc, out, t, _ = self.cli(ROUTES, "search", "sea", "--sources", "wikimedia,coverr", "--delay", "0",
                                 "--retry-failed", "--save", str(save))
        self.assertEqual(rc, 0)
        self.assertFalse([u for u in t.urls() if "coverr.co" in u])  # coverr answered last time
        data = json.loads(save.read_text(encoding="utf-8"))
        self.assertEqual(data["sources"]["coverr"]["status"], "cached")
        self.assertEqual(data["sources"]["wikimedia"]["status"], "ok")
        ids = {r["id"].split(":")[0] for r in data["results"]}
        self.assertEqual(ids, {"coverr", "wikimedia"})
        self.assertEqual(len(data["searches"]), 2)
        self.assertIn("coverr     cached", out)
        rc, out, t, _ = self.cli(ROUTES, "search", "sea", "--sources", "wikimedia,coverr", "--retry-failed",
                                 "--save", str(save))
        self.assertEqual((rc, t.calls), (0, []))  # both answered now: nothing is asked again
        self.assertIn("nothing was asked again", out)

    def test_retry_failed_with_replace_keeps_the_skipped_sources_results(self):
        """`--retry-failed --replace` said 'its results stay in the file' and then saved 0 of them."""
        save = self.dir / "r.json"
        self.cli([(r"commons\.wikimedia\.org", (429, "slow", {"Retry-After": "600"}))] + ROUTES,
                 "search", "sea", "--sources", "wikimedia,coverr", "--delay", "0", "--save", str(save))
        self.cli(ROUTES, "search", "night", "--sources", "nasa", "--delay", "0", "--save", str(save))  # another query
        coverr = sorted(r["id"] for r in json.loads(save.read_text(encoding="utf-8"))["results"]
                        if r["source"] == "coverr" and r["query"] == "sea")
        self.assertTrue(coverr)
        rc, out, t, _ = self.cli(ROUTES, "search", "sea", "--sources", "wikimedia,coverr", "--delay", "0",
                                 "--retry-failed", "--replace", "--save", str(save))
        self.assertEqual(rc, 0)
        self.assertFalse([u for u in t.urls() if "coverr.co" in u])
        self.assertIn("its results stay in the file (--retry-failed)", out)
        data = json.loads(save.read_text(encoding="utf-8"))
        self.assertEqual(sorted(r["id"] for r in data["results"] if r["source"] == "coverr"), coverr)
        self.assertTrue(any(r["source"] == "wikimedia" for r in data["results"]))
        self.assertEqual({r["query"] for r in data["results"]}, {"sea"})  # the other query's results were replaced
        self.assertEqual(len(data["searches"]), 1)


class Archive5xxTest(TempDirCase):
    """`download archive:Flickr-8633486122` failed once with HTTP 500 from a data node and worked on a retry."""

    def test_one_retry_on_a_data_node_500(self):
        calls = []

        def node(req):
            calls.append(req.full_url)
            if len(calls) == 1:  # urllib followed the redirect to the data node, which answered 500
                raise urllib.error.HTTPError("https://dn000000.ca.archive.org/0/items/synthetic-coast-film/x.mov", 500,
                                             "Internal Server Error", email.message.Message(), io.BytesIO(b""))
            return OK_MP4
        h, _, sleeps = http([(r"archive\.org/download", node)] + ROUTES)
        with mock.patch.object(FF, "measure", return_value={}):
            r = FF.download_one(h, DB, "archive:synthetic-coast-film", self.out,
                                {"results": self.dir / "none.json", "max_mb": 300})
        self.assertEqual((len(calls), len(sleeps)), (2, 1))
        self.assertTrue((self.out / r["file"]).is_file())
        h, t, _ = http([(r".", (500, "x"))])
        with self.assertRaisesRegex(FF.HttpError, "server error, again after one retry"):
            h.get_text("https://archive.org/download/a/b.mov")
        self.assertEqual(len(t.calls), 2)
        h, t, _ = http([(r".", (500, "x"))])
        with self.assertRaises(FF.HttpError):
            h.get_text("https://example.org/x")
        self.assertEqual(len(t.calls), 1)  # elsewhere a 500 is not retried

    def test_retry_after_on_a_5xx_is_bounded_like_a_429(self):
        """A 502 with Retry-After 86400 slept a day, and an HTTP-date one about 73 years: the server never decides."""
        far = email.utils.format_datetime(datetime.datetime(2099, 10, 21, 7, 28, tzinfo=datetime.timezone.utc))
        for status, ra in ((502, "86400"), (500, far), (504, "901")):
            h, t, sleeps = http([(r".", (status, "x", {"Retry-After": ra}))])
            with self.assertRaisesRegex(FF.HttpError, r"server error; Retry-After \d+s is too long for --wait-429 30 "
                                                      r"\(longer than --wait-429 can wait \(900 s\): try later\)"):
                h.get_text("https://ia800.us.archive.org/0/items/a/b.mov")
            self.assertEqual((len(t.calls), sleeps), (1, []), (status, ra))
        h, t, sleeps = http([(r".", (502, "x", {"Retry-After": "120"}))])
        with self.assertRaisesRegex(FF.HttpError, r"rerun with --wait-429 120"):
            h.get_text("https://archive.org/download/a/b.mov")
        self.assertEqual((len(t.calls), sleeps), (1, []))
        h, t, sleeps = http([(r".", (502, "x", {"Retry-After": "120"}))])
        h.max_retry_after = 300  # --wait-429 300 allows it: one wait of what the server asked, then one retry
        with self.assertRaisesRegex(FF.HttpError, "server error, again after one retry"):
            h.get_text("https://archive.org/download/a/b.mov")
        self.assertEqual((len(t.calls), sleeps), (2, [120.0]))
        h, t, sleeps = http([(r".", (502, "x", {"Retry-After": "3"}))])
        with self.assertRaises(FF.HttpError):
            h.get_text("https://archive.org/download/a/b.mov")
        self.assertEqual((len(t.calls), sleeps), (2, [3.0]))


def suspicious_meta(req):
    ident = urllib.parse.unquote(req.full_url.rsplit("/", 1)[-1])
    docs = {d["identifier"]: d for d in json.loads(fixture("archive_search_suspicious.json"))["response"]["docs"]}
    meta = json.loads(fixture("archive_meta.json"))
    doc = docs.get(ident, {})
    meta["metadata"].update(identifier=ident, licenseurl=doc.get("licenseurl"), title=doc.get("title", ident))
    return (200, json.dumps(meta), {})


SUSPICIOUS_ROUTES = [(r"archive\.org/advancedsearch\.php", fixture("archive_search_suspicious.json")),
                     (r"archive\.org/metadata/", suspicious_meta)]


class ArchiveSuspiciousTest(TempDirCase):
    """`search "heavy rain"` kept 'Prince - Musicology (Official Music Video)' as CC BY 4.0 | commercial ok."""
    BAD = ("archive:youtube-SYNTHabc123", "archive:y-2mate.so-top-20-synthetic-moments-of-a-game",
           "archive:synthetic-whale-movie-music-video-1993-hd-vhs-rip")

    def test_patterns(self):
        s = FF.archive_licence_suspicion
        self.assertEqual(s("youtube-zILabWVdIMs", "Prince - Musicology (Official Music Video)"), "YouTube re-upload")
        self.assertEqual(s("y-2mate.so-top-20-satisfying-deaths-of-hated-video-game-characters", ""), "downloader rip")
        self.assertEqual(s("free-willy-movie-michael-jackson-purple-rain-music-video-1993-hd-vhs-rip", ""), "music video")
        self.assertEqual(s("some-show", "Some Show S01E02 full episode"), "film or TV rip")
        self.assertIsNone(s("Flickr-8633486122", "Lettuce emerging"))
        self.assertIsNone(s("duck_and_cover_1951", "Duck and Cover (1951)"))
        self.assertIsNone(s("home-movies-1950s", "Home movies of a garden"))  # "movies" is not "movie"

    def test_search_flags_them_and_commercial_drops_them(self):
        h, _, _ = http(SUSPICIOUS_ROUTES)
        rep = FF.run_search(h, DB, "rain", ["archive"], 10, {})
        by = {r["id"]: r for r in rep["results"]}
        for rid in self.BAD:
            lic = by[rid]["licence"]
            self.assertIn("suspicious-licence", by[rid]["flags"], rid)
            self.assertIsNone(lic["commercial"], rid)
            self.assertFalse(lic["verified"], rid)
            self.assertIn("uploader's licence claim", lic["note"])
        ok = by["archive:Flickr-0000000001"]
        self.assertIs(ok["licence"]["commercial"], True)
        self.assertEqual(ok["flags"], ["uploader-licence"])
        self.assertIn("trust the uploader?", ok["licence"]["note"])
        self.assertEqual(ok["thumb_url"], "https://archive.org/services/img/Flickr-0000000001")
        self.assertTrue(any("3 look like music videos" in w for w in rep["warnings"]))
        with mock.patch("sys.stdout", new_callable=io.StringIO) as so:
            FF.print_results(rep)
        self.assertIn("CC BY 4.0 SUSPICIOUS (uploader's claim) | commercial ?", so.getvalue())
        self.assertIn("CC BY 2.0 (uploader's claim) | commercial ok", so.getvalue())
        h, _, _ = http(SUSPICIOUS_ROUTES)
        rep = FF.run_search(h, DB, "rain", ["archive"], 10, {"commercial": True})
        self.assertEqual([r["id"] for r in rep["results"]], ["archive:Flickr-0000000001"])
        self.assertEqual(rep["sources"]["archive"]["dropped"], {"suspicious uploader licence (music video, film or rip)": 3})

    def test_download_with_commercial_refuses_them(self):
        h, _, _ = http([(r"archive\.org/download", OK_MP4)] + SUSPICIOUS_ROUTES)
        with self.assertRaisesRegex(FF.FootageError, "suspicious uploader licence"):
            FF.download_one(h, DB, "archive:youtube-SYNTHabc123", self.out,
                            {"results": self.dir / "none.json", "max_mb": 300, "commercial": True})

    def test_an_older_results_record_is_checked_again(self):
        """Results are kept across searches, so a record saved before the check still said CC BY | commercial ok
        and passed `download --commercial` without a new request."""
        ident, title = "youtube-SYNTHabc123", "Synthetic Band - Song (Official Music Video)"
        old = {"id": f"archive:{ident}", "source": "archive", "source_name": "Internet Archive", "title": title,
               "page_url": f"https://archive.org/details/{ident}", "file_url": f"https://archive.org/download/{ident}/x.mp4",
               "width": 640, "height": 360, "bytes": 10_000_000, "query": "rain", "attribution": "x", "flags": [],
               "licence": FF.classify_licence(None, "https://creativecommons.org/licenses/by/4.0/")}
        save = self.dir / "last_search.json"
        save.write_text(json.dumps({"schema": FF.RESULTS_SCHEMA, "query": "rain", "searched_at": "2026-10-28T10:00:00Z",
                                    "sources": {"archive": {"status": "ok", "count": 1}}, "results": [old]}),
                        encoding="utf-8")
        h, t, _ = http([(r"archive\.org/download", OK_MP4)])
        with self.assertRaisesRegex(FF.FootageError, "CC BY 4.0 suspicious uploader licence"):
            FF.download_one(h, DB, old["id"], self.out, {"results": save, "max_mb": 300, "commercial": True})
        self.assertEqual(t.calls, [])
        with mock.patch.object(FF, "make_http", lambda args: h), mock.patch("sys.stdout", new_callable=io.StringIO), \
                mock.patch("sys.stderr", new_callable=io.StringIO) as se:
            rc = FF.main(["download", old["id"], "--out", str(self.out), "--results", str(save), "--commercial",
                          "--dry-run"])
        self.assertEqual(rc, 1)
        self.assertIn(f"{old['id']}\tFAILED", se.getvalue())
        self.assertIn("suspicious uploader licence", se.getvalue())
        FF.save_results(save, {"schema": FF.RESULTS_SCHEMA, "query": "ocean", "searched_at": "2026-10-29T10:00:00Z",
                               "sources": {}, "results": []})
        kept = next(r for r in json.loads(save.read_text(encoding="utf-8"))["results"] if r["id"] == old["id"])
        self.assertEqual(kept["flags"], ["suspicious-licence", "uploader-licence"])  # the merge repairs the file too
        self.assertIsNone(kept["licence"]["commercial"])
        self.assertIn("looks like a YouTube re-upload", kept["licence"]["note"])
        fresh = FF.recheck_archive_licence(kept)
        self.assertEqual(fresh, kept)  # idempotent
        clean = dict(old, id="archive:Flickr-1", title="Lettuce emerging")
        self.assertIs(FF.recheck_archive_licence(clean), clean)
        with mock.patch.object(FF, "measure", return_value={}):
            r = FF.download_one(h, DB, old["id"], self.out, {"results": save, "max_mb": 300})
        side = json.loads(FF.sidecar_for(self.out / r["file"]).read_text(encoding="utf-8"))
        self.assertIn("suspicious-licence", side["result"]["flags"])  # the sidecar does not say commercial ok
        self.assertIsNone(side["licence"]["commercial"])


class DropReasonTest(unittest.TestCase):
    """`dropped: 22 commercial use not allowed or not confirmed` did not separate Restricted from unread."""

    def test_counts_say_why(self):
        h, _, _ = http(ROUTES)
        rep = FF.run_search(h, DB, "sea", ["mixkit"], 10, {"commercial": True})
        self.assertEqual(rep["sources"]["mixkit"]["dropped"], {"Mixkit Restricted (personal use only)": 1})
        h, _, _ = http([(r"synthetic-night-walk", (500, "down"))] + ROUTES)
        rep = FF.run_search(h, DB, "sea", ["mixkit"], 10, {"commercial": True})
        self.assertEqual(rep["sources"]["mixkit"]["dropped"], {"Mixkit licence not read (the clip page did not answer)": 1})
        nc = {"licence": FF.classify_licence(None, "https://creativecommons.org/licenses/by-nc/4.0/"), "flags": []}
        self.assertEqual(FF.keep(nc, {"commercial": True}), "non-commercial licence")
        odd = {"licence": FF.classify_licence(None, "http://creativecommons.org/licenses/sampling+/1.0/"), "flags": []}
        self.assertEqual(FF.keep(odd, {"commercial": True}), "commercial use not confirmed")


class ResultsMergeTest(TempDirCase):
    """Each search overwrote last_search.json, so ids from earlier searches no longer resolved."""

    def search(self, *argv):
        fake = lambda args: FF.Http(delay=0, transport=Transport(ROUTES), sleep=lambda s: None)  # noqa: E731
        with mock.patch.object(FF, "make_http", fake), mock.patch.dict(os.environ, NO_KEYS), \
                mock.patch("sys.stdout", new_callable=io.StringIO) as so:
            self.assertEqual(FF.main(["search", *argv, "--save", str(self.dir / "last.json")]), 0)
        return json.loads((self.dir / "last.json").read_text(encoding="utf-8")), so.getvalue()

    def test_searches_merge_by_id(self):
        self.search("sea", "--sources", "coverr")
        data, out = self.search("night", "--sources", "wikimedia")
        self.assertEqual(data["query"], "night")  # the top level is the newest search, as before
        self.assertTrue(data["results"][0]["id"].startswith("wikimedia:"))
        self.assertEqual({r["id"].split(":")[0] for r in data["results"]}, {"coverr", "wikimedia"})
        self.assertEqual([s["query"] for s in data["searches"]], ["sea", "night"])
        self.assertIsNotNone(FF.pick_from_results(self.dir / "last.json", "coverr:AAAA111111"))
        self.assertIn("from earlier searches: 2 searches in the file", out)
        data, _ = self.search("sea", "--sources", "coverr", "--replace")
        self.assertEqual({r["id"].split(":")[0] for r in data["results"]}, {"coverr"})
        self.assertEqual(len(data["searches"]), 1)

    def test_an_older_file_and_a_read_mixkit_licence(self):
        old = {"schema": FF.RESULTS_SCHEMA, "query": "a", "searched_at": "2026-10-28T00:00:00Z", "sources": {},
               "results": [{"id": "mixkit:1", "source": "mixkit", "licence": {"name": FF.MIXKIT_FREE, "verified": True},
                            "query": "a"}, {"id": "nasa:x", "source": "nasa", "licence": {}, "query": "a"}]}
        new = {"schema": FF.RESULTS_SCHEMA, "query": "b", "sources": {},
               "results": [{"id": "mixkit:1", "source": "mixkit", "licence": {"verified": False}, "query": "b"}]}
        m = FF.merge_results(old, new)
        self.assertEqual([r["id"] for r in m["results"]], ["mixkit:1", "nasa:x"])
        self.assertEqual((m["results"][0]["licence"]["name"], m["results"][0]["query"]), (FF.MIXKIT_FREE, "b"))
        self.assertEqual([s["query"] for s in m["searches"]], ["a", "b"])  # a file without history gets one


class SizesAndCapsTest(TempDirCase):
    """`download mixkit:2066 --dry-run` did not say it would take 2160p at 68 MB, and there was no --quality."""

    def setUp(self):
        super().setUp()
        h, _, _ = http(ROUTES)
        with mock.patch.dict(os.environ, NO_KEYS):
            rep = FF.run_search(h, DB, "sea", ["wikimedia", "archive", "nasa", "coverr"], 10, {"allow_nd": True})
        rep["results"] += FF.parse_pexels(DB, json.loads(fixture("pexels_search.json")))
        rep["results"] += FF.parse_pixabay(DB, json.loads(fixture("pixabay_search.json")))
        self.results = self.dir / "r.json"
        self.results.write_text(json.dumps(rep), encoding="utf-8")

    def get(self, rid, routes, **opts):
        h, t, _ = http(list(routes) + ROUTES)
        with mock.patch.object(FF, "measure", return_value={}):
            r = FF.download_one(h, DB, rid, self.out, {"results": self.results, "max_mb": 300, **opts})
        side = None if r.get("dry_run") else json.loads(FF.sidecar_for(self.out / r["file"]).read_text(encoding="utf-8"))
        return r, side, t

    def test_dry_run_listed_sizes_and_head(self):
        r, _, t = self.get("wikimedia:9000002", [], dry_run=True)
        self.assertEqual((r["quality"], r["width"], r["height"], r["bytes"], r["size_from"]),
                         (1080, 1080, 1920, 4200000, "listed by the source"))
        self.assertEqual(t.calls, [])
        heads = [(r"~orig\.mp4", NO_FILE), (r"~large\.mp4", (200, b"", {"Content-Length": str(80 * 1048576)}))]
        r, _, t = self.get("nasa:SYNTH_20260101_Ocean_Orbit", heads, dry_run=True)
        self.assertTrue(r["file_url"].endswith("~large.mp4"))
        self.assertEqual((r["bytes"], r["size_from"]), (80 * 1048576, "HEAD"))
        self.assertIn("80.0 MB (HEAD)", FF._dry_text(r))
        big = [(r"~(orig|large|medium)\.mp4", (200, b"", {"Content-Length": str(80 * 1048576)}))]
        r, _, t = self.get("nasa:SYNTH_20260101_Ocean_Orbit", big, dry_run=True, max_mb=50)
        self.assertEqual(len(t.calls), 3)  # each variant asked once, the smallest reported
        self.assertTrue(r["file_url"].endswith("~medium.mp4"))
        self.assertTrue(r["over_max_mb"])  # every variant is over the cap: said, not hidden
        self.assertIn("OVER --max-mb", FF._dry_text(r))

    def test_quality_and_max_height(self):
        ok = [(r"videos\.pexels\.com|cdn\.pixabay\.com|archive\.org/download", OK_MP4)]
        _, side, t = self.get("pexels:1000001", ok, max_quality=1080)
        self.assertTrue(side["result"]["file_url"].endswith("1000001-hd_1080_1920_25fps.mp4"))
        self.assertEqual((side["result"]["width"], side["result"]["height"], side["result"]["quality"]), (1080, 1920, 1080))
        self.assertNotIn("smaller-variant", side["result"]["flags"])
        shutil.rmtree(self.out)
        _, side, _ = self.get("pexels:1000001", ok, max_height=1280)
        self.assertTrue(side["result"]["file_url"].endswith("sd_360_640_25fps.mp4"))
        _, side, _ = self.get("pixabay:2000001", ok, max_quality=540)
        self.assertTrue(side["result"]["file_url"].endswith("2000001-small.mp4"))
        _, side, t = self.get("archive:synthetic-coast-film", ok, max_quality=360)
        self.assertTrue(side["result"]["file_url"].endswith("Coast%20Film%20Original.mp4"))  # 640x360, not the .mov
        with self.assertRaisesRegex(FF.FootageError, r"its file is 1920x3412, over --quality 1080 \(Coverr offers no smaller"):
            self.get("coverr:BBBB222222", [], max_quality=1080)
        r, _, _ = self.get("nasa:SYNTH_20260101_Ocean_Orbit", [(r"~orig\.mp4", OK_MP4)], max_quality=1080)
        self.assertIn("--quality 1080 not checked", r["note"])

    def test_full_range_quicktime_is_flagged_in_the_sidecar(self):
        m = {"width": 1920, "height": 1080, "codec": "mjpeg", "pix_fmt": "yuvj420p", "color_range": "pc",
             "container": "mov,mp4,m4a,3gp,3g2,mj2"}
        h, _, _ = http([(r"archive\.org/download", OK_MP4)] + ROUTES)
        with mock.patch.object(FF, "measure", return_value=m):
            r = FF.download_one(h, DB, "archive:synthetic-coast-film", self.out, {"results": self.results, "max_mb": 300})
        side = json.loads(FF.sidecar_for(self.out / r["file"]).read_text(encoding="utf-8"))
        self.assertTrue(r["file"].endswith(".mov"))
        self.assertIn("full-range", side["result"]["flags"])
        self.assertIn("full-range QuickTime video (yuvj420p, color_range pc)", side["warnings"][0])
        self.assertIn("scale=in_range=pc:out_range=tv", side["warnings"][0])
        self.assertEqual(r["warnings"], side["warnings"])
        self.assertEqual(FF.range_warnings({"pix_fmt": "yuv420p", "color_range": "tv"}, "a.mp4"), [])

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "needs ffmpeg")
    def test_measure_reads_the_pixel_format_and_range(self):
        src = self.dir / "fr.mov"
        made = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-f", "lavfi", "-i", "testsrc=duration=1:size=160x90:rate=5",
                               "-c:v", "mjpeg", "-pix_fmt", "yuvj420p", str(src)], capture_output=True, timeout=60)
        if made.returncode:
            self.skipTest("this ffmpeg cannot write mjpeg")
        m = FF.measure(src)
        self.assertEqual(m.get("pix_fmt"), "yuvj420p")
        self.assertTrue(FF.range_warnings(m, src.name))


class CreditsPathTest(unittest.TestCase):
    """ATTRIBUTION.md said `run python3 scripts/free_footage.py credits <this folder>`, which fails from the root."""

    def test_the_header_names_a_path_that_works_from_the_repo_root(self):
        with tempfile.TemporaryDirectory() as d:
            text = FF.credits_markdown(Path(d))
        m = re.search(r"run `python3 (\S+) credits <this folder>` from the repository root", text)
        self.assertIsNotNone(m, text[:300])
        self.assertTrue((SK.parents[2] / m.group(1)).is_file())
        self.assertNotIn("`python3 scripts/free_footage.py", text)


JPEG = b"\xff\xd8\xff\xe0\x00\x10JFIF\x00" + b"\x00" * 200


class PreviewTest(TempDirCase):
    """No thumbnail or preview links were recorded, so clips could not be screened for people or text first."""

    def setUp(self):
        super().setUp()
        lic = FF.source_licence("coverr", FF.sources_by_id(DB)["coverr"])
        mk = lambda nid, **kw: FF.make_result(DB, "coverr", nid, title=kw.pop("title", f"Clip {nid}"),  # noqa: E731
                                              page_url=f"https://coverr.co/videos/{nid}",
                                              file_url=f"https://cdn.example.org/{nid}.mp4", licence=lic,
                                              width=1920, height=1080, **kw)
        recs = [mk("A1", title='Rain & "leaf" <x', thumb_url="https://img.example.org/a.jpg"),
                mk("B1", thumb_url="https://img.example.org/b.jpg"), mk("C1"),
                mk("D1", preview_url="https://cdn.example.org/d-360p.mp4")]
        self.results = self.dir / "r.json"
        self.results.write_text(json.dumps({"schema": FF.RESULTS_SCHEMA, "query": "rain", "results": recs}), encoding="utf-8")

    def routes(self, extra=()):
        return list(extra) + [(r"img\.example\.org/a\.jpg", (200, JPEG, {"Content-Type": "image/jpeg"})),
                              (r"img\.example\.org/b\.jpg", (200, "<html>no</html>", {"Content-Type": "text/html"}))]

    def test_html_sheet_without_ffmpeg(self):
        h, t, _ = http(self.routes())
        with mock.patch.object(FF.shutil, "which", return_value=None):
            s = FF.build_preview(h, FF.preview_items(self.results), self.dir / "pv")
        rows = {r["id"]: r for r in s["items"]}
        self.assertEqual(rows["coverr:A1"]["from"], "thumbnail")
        self.assertEqual((self.dir / "pv" / rows["coverr:A1"]["image"]).read_bytes(), JPEG)
        self.assertIn("did not answer with an image", rows["coverr:B1"]["errors"][0])
        self.assertIsNone(rows["coverr:C1"]["image"])
        self.assertIsNone(rows["coverr:D1"]["image"])  # its preview video needs ffmpeg
        self.assertIsNone(s["jpg"])
        html = (self.dir / "pv" / "contact_sheet.html").read_text(encoding="utf-8")
        self.assertIn("Rain &amp; &quot;leaf&quot; &lt;x", html)
        self.assertNotIn('"leaf" <x', html)
        self.assertFalse([u for u in t.urls() if "cdn.example.org" in u])  # never a clip
        self.assertEqual(json.loads((self.dir / "pv" / "contact_sheet.json").read_text(encoding="utf-8"))["schema"],
                         "kosif.free_footage.preview.v1")
        self.assertEqual([r[0]["id"] for r in FF.preview_items(self.results, ids=["coverr:C1"])], ["coverr:C1"])

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "needs ffmpeg")
    def test_jpg_sheet_and_strips_with_ffmpeg(self):
        jpg, mp4 = self.dir / "a.jpg", self.dir / "d.mp4"
        for args in (["-f", "lavfi", "-i", "color=c=red:s=640x360", "-frames:v", "1", str(jpg)],
                     ["-f", "lavfi", "-i", "testsrc=duration=3:size=320x180:rate=10", "-pix_fmt", "yuv420p", str(mp4)]):
            subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", *args], check=True, capture_output=True, timeout=60)
        routes = self.routes([(r"img\.example\.org/a\.jpg", (200, jpg.read_bytes(), {"Content-Type": "image/jpeg"})),
                              (r"cdn\.example\.org/d-360p\.mp4", (200, mp4.read_bytes(), {"Content-Type": "video/mp4"}))])
        h, t, _ = http(routes)
        s = FF.build_preview(h, FF.preview_items(self.results), self.dir / "pv")
        rows = {r["id"]: r for r in s["items"]}
        self.assertEqual((rows["coverr:A1"]["from"], rows["coverr:D1"]["from"]), ("thumbnail", "preview video"))
        self.assertEqual(s["jpg"], "contact_sheet.jpg")
        sheet = FF.measure(self.dir / "pv" / "contact_sheet.jpg")
        self.assertEqual((sheet.get("width"), sheet.get("height")), (4 * 320 + 3 * 4 + 2 * 4, 180 + 2 * 4))
        self.assertFalse(list((self.dir / "pv").rglob("*.preview.mp4")))  # the preview file is deleted after use
        self.assertFalse((self.dir / "pv" / "cells").exists())
        h, _, _ = http(routes)
        s3 = FF.build_preview(h, FF.preview_items(self.results, ids=["coverr:D1"]), self.dir / "pv3", frames=3)
        strip = FF.measure(self.dir / "pv3" / s3["items"][0]["image"])
        self.assertEqual((strip.get("width"), strip.get("height")), (960, 180))

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "needs ffmpeg")
    def test_thumbnails_in_mixed_pixel_formats_all_reach_the_sheet(self):
        # live 2026-10-29: Archive thumbnails came as yuvj420p and yuvj422p; the format change restarted ffmpeg's
        # tile filter and a 6-cell sheet showed only cells 5 and 6
        imgs = {}
        for name, colour, fmt in (("a", "red", "yuvj420p"), ("b", "blue", "yuvj422p"), ("c", "green", "yuvj420p")):
            p = self.dir / f"{name}.jpg"
            subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c={colour}:s=640x360",
                            "-frames:v", "1", "-pix_fmt", fmt, str(p)], check=True, capture_output=True, timeout=60)
            imgs[name] = p.read_bytes()
        lic = FF.source_licence("coverr", FF.sources_by_id(DB)["coverr"])
        recs = [FF.make_result(DB, "coverr", k, title=k, page_url=f"https://coverr.co/videos/{k}", file_url="https://x/y.mp4",
                               licence=lic, thumb_url=f"https://img.example.org/{k}.jpg") for k in imgs]
        items = [(r, None) for r in recs]
        h, _, _ = http([(rf"img\.example\.org/{k}\.jpg", (200, v, {"Content-Type": "image/jpeg"})) for k, v in imgs.items()])
        s = FF.build_preview(h, items, self.dir / "pv")
        raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", str(self.dir / "pv" / s["jpg"]), "-f", "rawvideo",
                              "-pix_fmt", "rgb24", "-"], check=True, capture_output=True, timeout=60).stdout
        width = 4 * 320 + 3 * 4 + 2 * 4

        def pixel(cell):
            x, y = 4 + cell * (320 + 4) + 160, 4 + 90
            return tuple(raw[(y * width + x) * 3:(y * width + x) * 3 + 3])
        r, g, b = pixel(0)
        self.assertTrue(r > 200 and g < 60 and b < 60, pixel(0))
        r, g, b = pixel(1)
        self.assertTrue(b > 200 and r < 60 and g < 60, pixel(1))
        r, g, b = pixel(2)
        self.assertTrue(g > 90 and r < 60 and b < 60, pixel(2))

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "needs ffmpeg")
    def test_a_folder_of_downloads_uses_the_local_clips(self):
        self.out.mkdir()
        clip = self.out / "coverr-A1.mp4"
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "lavfi", "-i",
                        "testsrc=duration=2:size=320x180:rate=10", "-pix_fmt", "yuv420p", str(clip)],
                       check=True, capture_output=True, timeout=60)
        rec = json.loads(self.results.read_text(encoding="utf-8"))["results"][0]
        FF.sidecar_for(clip).write_text(json.dumps({"schema": FF.ASSET_SCHEMA, "file": clip.name, "result": rec,
                                                    "licence": rec["licence"]}), encoding="utf-8")
        fake = lambda args: FF.Http(delay=0, transport=Transport([]), sleep=lambda s: None)  # noqa: E731
        with mock.patch.object(FF, "make_http", fake), mock.patch("sys.stdout", new_callable=io.StringIO) as so:
            self.assertEqual(FF.main(["preview", str(self.out)]), 0)
        data = json.loads((self.out / "preview" / "contact_sheet.json").read_text(encoding="utf-8"))
        self.assertEqual(data["items"][0]["from"], "the downloaded clip")
        self.assertIn("# contact sheet:", so.getvalue())


class ThumbAndPreviewFieldsTest(unittest.TestCase):
    def test_every_adapter_records_them(self):
        cv, _ = FF.parse_coverr(DB, fixture("coverr_search.html"))
        self.assertEqual(cv[0]["preview_url"], "https://cdn.coverr.co/videos/coverr-synthetic-calm-waves-1111/360p.mp4")
        self.assertEqual(cv[1]["preview_url"], "https://cdn.coverr.co/videos/coverr-synthetic-waves-near-the-coast-2222/360p.mp4")
        px = FF.parse_pexels(DB, json.loads(fixture("pexels_search.json")))[0]
        self.assertEqual(px["thumb_url"], "https://images.pexels.com/videos/1000001/synthetic.jpeg")
        self.assertTrue(px["preview_url"].endswith("sd_360_640_25fps.mp4"))
        self.assertEqual([v["quality"] for v in px["variants"]], [2160, 1080, 360])
        pb = FF.parse_pixabay(DB, json.loads(fixture("pixabay_search.json")))[0]
        self.assertTrue(pb["thumb_url"].endswith("2000001-medium.jpg"))
        self.assertTrue(pb["preview_url"].endswith("2000001-tiny.mp4"))
        self.assertEqual([(v["width"], v["bytes"]) for v in pb["variants"]], [(1280, 5242880), (960, 2621440), (640, 1048576)])
        asset = json.loads(fixture("nasa_asset.json"))
        doc = FF.parse_nasa_search(json.loads(fixture("nasa_search.json")))[0]
        vids, _ = FF.nasa_variants(asset)
        nasa = FF.nasa_result(DB, doc, vids[0], alternates=vids, preview=FF.nasa_preview(asset))
        self.assertTrue(nasa["thumb_url"].endswith("~large.jpg"))
        self.assertTrue(nasa["preview_url"].startswith("https://") and nasa["preview_url"].endswith("~preview.mp4"))
        arch = FF.archive_result(DB, {"identifier": "synthetic-coast-film"}, json.loads(fixture("archive_meta.json")))
        self.assertEqual(arch["thumb_url"], "https://archive.org/services/img/synthetic-coast-film")
        wm = json.loads(fixture("wikimedia_search.json"))
        wm["query"]["pages"][0]["imageinfo"][0]["thumburl"] = \
            "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/H.webm/480px--H.webm.jpg?utm_source=x"
        w = {r["id"]: r for r in FF.parse_wikimedia(DB, wm)}
        self.assertEqual(w["wikimedia:9000002"]["thumb_url"],
                         "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/H.webm/480px--H.webm.jpg")
        self.assertIsNone(w["wikimedia:9000001"]["thumb_url"])
        self.assertIn("iiurlwidth=480", FF.commons_search_url("sea", 5))
        mk = FF.parse_mixkit(DB, fixture("mixkit_discover.html"))[0]
        self.assertEqual(mk["thumb_url"], "https://assets.mixkit.co/videos/40001/40001-thumb-360-0.jpg")
        for rec in (cv[2], px, pb, nasa, arch, mk):
            self.assertIn("thumb_url", rec)
            self.assertIn("preview_url", rec)

    def test_cli_help_lists_the_new_options(self):
        run = lambda *a: subprocess.run([sys.executable, str(SCRIPT), *a], capture_output=True, text=True, timeout=60)  # noqa: E731
        self.assertIn("preview", run("--help").stdout)
        self.assertEqual(run("preview", "--help").returncode, 0)
        search = run("search", "--help").stdout
        for opt in ("--resolve", "--match", "--no-people", "--retry-failed", "--replace", "--wait-429",
                    "--retry-challenge"):
            self.assertIn(opt, search)
        self.assertIn("reads each Mixkit clip page", search)
        download = run("download", "--help").stdout
        for opt in ("--quality", "--max-height", "--wait-429", "--retry-challenge"):
            self.assertIn(opt, download)


if __name__ == "__main__":
    unittest.main()
