"""Free footage, offline: the sources database (schema, uniqueness, templates), licence extraction, attribution
formatting, every search adapter against hand-written synthetic answers shaped like each API or page, key gating,
the rate limit, size caps, downloads with sidecars and ATTRIBUTION.md. urlopen is replaced for the whole module,
so nothing leaves the machine.

    python3 -m unittest discover -s .claude/skills/kosif-superpowers/evals -p 'test_free_footage.py' -v
"""
import email.message
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
import urllib.error
import urllib.parse
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


class Transport:
    """Routes a request URL (regex) to (status, body, headers); records every call; refuses unknown URLs."""

    def __init__(self, routes):
        self.routes = list(routes)
        self.calls = []

    def __call__(self, req, timeout):
        url = req.full_url
        self.calls.append((url, dict(req.header_items()), timeout))
        for rx, answer in self.routes:
            if re.search(rx, url):
                if callable(answer):
                    answer = answer(req)
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
        self.assertEqual(rows[0]["page_url"], "https://mixkit.co/free-stock-video/synthetic-gulls-over-the-sea-30001/")
        self.assertEqual((rows[0]["width"], rows[0]["height"]), (1280, 720))

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
        h, t, _ = http(ROUTES)
        r = FF.download_one(h, DB, "coverr:AAAA111111", self.out, self.opts(dry_run=True))
        self.assertTrue(r["dry_run"])
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
        routes = [(r"pexels\.com/search", (403, "")), (r"api\.pexels\.com", (401, "")),
                  (r"commons\.wikimedia\.org", "{}"), (r"upload\.wikimedia\.org", (429, "", {"Retry-After": "600"})),
                  (r"mixkit\.co", (206, MP4)), (r"videvo\.net", (403, ""))]
        h, _, _ = http(routes)
        rep = FF.run_probe(h, DB, ["pexels", "wikimedia", "mixkit", "videvo"])
        st = {s["id"]: s for s in rep["sources"]}
        self.assertEqual(st["pexels"]["status"], "needs-key")
        self.assertEqual(st["wikimedia"]["status"], "partial")
        self.assertEqual(st["mixkit"]["status"], "ok")
        self.assertEqual(st["videvo"]["status"], "blocked")
        self.assertFalse(st["pexels"]["changed"])
        self.assertEqual(rep["schema"], FF.PROBE_SCHEMA)

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


if __name__ == "__main__":
    unittest.main()
