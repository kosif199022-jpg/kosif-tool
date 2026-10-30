"""Free photos, offline: every adapter against hand-written answers shaped like each API, licence filters, key
gating, results merging, the contact sheet, downloads with sidecars and ATTRIBUTION.md. urlopen is blocked for the
whole module and HTTP goes through a fake transport, so nothing leaves the machine.

    python3 -m unittest discover -s .claude/skills/kosif-superpowers/evals -p 'test_free_photos.py' -v
"""
import io
import json
import sys
import tempfile
import unittest
import urllib.error
import urllib.parse
from pathlib import Path
from unittest import mock

SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK / "scripts"))
import free_footage as FF  # noqa: E402
import free_photos as FP  # noqa: E402

JPG = b"\xff\xd8\xff\xe0\x00\x10JFIF" + b"\x00" * 2000
NO_KEYS = {}
_PATCH = None


def setUpModule():
    global _PATCH
    _PATCH = mock.patch("urllib.request.urlopen", side_effect=AssertionError("a test tried to reach the network"))
    _PATCH.start()


def tearDownModule():
    _PATCH.stop()


class Resp(io.BytesIO):
    def __init__(self, body, status=200, url=""):
        super().__init__(body)
        self.status, self.headers, self._url = status, {}, url

    def geturl(self):
        return self._url


class Fake:
    """A transport answering by URL prefix; records each request."""

    def __init__(self, routes):
        self.routes, self.seen = routes, []

    def __call__(self, req, timeout):
        url = req.full_url
        self.seen.append((url, dict(req.header_items())))
        for prefix, body in self.routes.items():
            if url.startswith(prefix):
                return Resp(body if isinstance(body, bytes) else json.dumps(body).encode(), url=url)
        raise urllib.error.URLError(f"no route in the fake for {url}")


def http(routes):
    t = Fake(routes)
    return FF.Http(delay=0, transport=t, sleep=lambda s: None), t


OPENVERSE = {"results": [
    {"id": "aaa-1", "title": "Desert dunes", "url": "https://live.staticflickr.com/1/a.jpg",
     "thumbnail": "https://api.openverse.org/v1/images/aaa-1/thumb/", "foreign_landing_url": "https://www.flickr.com/photos/x/1",
     "creator": "Sam", "creator_url": "https://www.flickr.com/photos/x", "license": "by", "license_version": "2.0",
     "license_url": "https://creativecommons.org/licenses/by/2.0/", "provider": "flickr", "source": "flickr",
     "width": 4000, "height": 2000},
    {"id": "aaa-2", "title": "Old map", "url": "https://example.org/b.jpg", "foreign_landing_url": "https://example.org/b",
     "license": "pdm", "license_version": "1.0", "license_url": "https://creativecommons.org/publicdomain/mark/1.0/",
     "provider": "museum", "width": 1000, "height": 1500},
    {"id": "aaa-3", "title": "NC photo", "url": "https://example.org/c.jpg", "foreign_landing_url": "https://example.org/c",
     "license": "by-nc", "license_version": "4.0", "license_url": "https://creativecommons.org/licenses/by-nc/4.0/",
     "provider": "flickr", "width": 3000, "height": 2000},
    {"id": "aaa-4", "title": "ND photo", "url": "https://example.org/d.jpg", "foreign_landing_url": "https://example.org/d",
     "license": "by-nd", "license_version": "4.0", "license_url": "https://creativecommons.org/licenses/by-nd/4.0/",
     "provider": "flickr", "width": 3000, "height": 2000},
]}

COMMONS = {"query": {"pages": [
    {"pageid": 11, "index": 2, "title": "File:Sphinx.jpg", "imageinfo": [{
        "url": "https://upload.wikimedia.org/s.jpg?utm_source=x", "descriptionurl": "https://commons.wikimedia.org/wiki/File:Sphinx.jpg",
        "thumburl": "https://upload.wikimedia.org/thumb/s.jpg", "width": 2560, "height": 1626, "mime": "image/jpeg",
        "extmetadata": {"LicenseShortName": {"value": "Public domain"}, "Artist": {"value": "<a href='x'>David Roberts</a>"},
                        "ObjectName": {"value": "The Great Sphinx"}, "AttributionRequired": {"value": "false"}}}]},
    {"pageid": 12, "index": 1, "title": "File:Logo.svg", "imageinfo": [{"url": "https://upload.wikimedia.org/l.svg",
                                                                          "mime": "image/svg+xml"}]},
    {"pageid": 13, "index": 3, "title": "File:Giza.jpg", "imageinfo": [{
        "url": "https://upload.wikimedia.org/g.jpg", "descriptionurl": "https://commons.wikimedia.org/wiki/File:Giza.jpg",
        "width": 5400, "height": 3605, "mime": "image/jpeg",
        "extmetadata": {"LicenseShortName": {"value": "CC BY-SA 4.0"},
                        "LicenseUrl": {"value": "https://creativecommons.org/licenses/by-sa/4.0"},
                        "Artist": {"value": "Ahmed"}}}]},
]}}

NASA = {"collection": {"items": [{"data": [{"nasa_id": "iss 01", "title": "Nile at night", "center": "JSC",
                                            "media_type": "image"}],
                                  "links": [{"href": "http://images-assets.nasa.gov/image/iss 01/iss 01~medium.jpg",
                                             "render": "image", "rel": "alternate", "width": 1280, "height": 853},
                                            {"href": "http://images-assets.nasa.gov/image/iss 01/iss 01~orig.jpg",
                                             "render": "image", "rel": "canonical", "width": 6048, "height": 4032}]}]}}

MET_SEARCH = {"total": 3, "objectIDs": [1, 2, 3]}
MET_OBJ = {
    1: {"objectID": 1, "isPublicDomain": True, "primaryImage": "https://images.metmuseum.org/o/1.jpg",
        "primaryImageSmall": "https://images.metmuseum.org/s/1.jpg", "title": "Qur'an folio", "objectDate": "9th c.",
        "culture": "Abbasid", "objectURL": "https://www.metmuseum.org/art/collection/search/1"},
    2: {"objectID": 2, "isPublicDomain": False, "primaryImage": "https://images.metmuseum.org/o/2.jpg", "title": "Rights"},
    3: {"objectID": 3, "isPublicDomain": True, "primaryImage": "", "title": "No image"},
}

PEXELS = {"photos": [{"id": 77, "width": 3000, "height": 4500, "url": "https://www.pexels.com/photo/x-77/",
                      "photographer": "Lina", "photographer_url": "https://www.pexels.com/@lina", "alt": "Night street",
                      "src": {"original": "https://images.pexels.com/77.jpeg", "large2x": "https://images.pexels.com/77-l.jpeg",
                              "medium": "https://images.pexels.com/77-m.jpeg"}}]}

PIXABAY = {"hits": [{"id": 5, "pageURL": "https://pixabay.com/photos/5/", "tags": "sea, wave", "user": "bob",
                     "largeImageURL": "https://pixabay.com/get/5_1280.jpg", "webformatURL": "https://pixabay.com/get/5_640.jpg",
                     "imageWidth": 6000, "imageHeight": 4000}]}

UNSPLASH = {"results": [
    {"id": "u1", "width": 4000, "height": 6000, "alt_description": "a mosque at dusk",
     "urls": {"raw": "https://images.unsplash.com/p1?ixid=1", "full": "https://images.unsplash.com/p1?full",
              "small": "https://images.unsplash.com/p1?small"},
     "links": {"html": "https://unsplash.com/photos/u1", "download_location": "https://api.unsplash.com/photos/u1/download"},
     "user": {"name": "Omar", "links": {"html": "https://unsplash.com/@omar"}}},
    {"id": "u2", "premium": True, "urls": {"full": "https://plus.unsplash.com/x"}, "links": {}, "user": {}},
]}


class Adapters(unittest.TestCase):
    def test_openverse_licences(self):
        rs = FP.parse_openverse(OPENVERSE)
        by = {r["id"]: r for r in rs}
        self.assertEqual(by["openverse:aaa-1"]["licence"]["name"], "CC BY 2.0")
        self.assertTrue(by["openverse:aaa-1"]["licence"]["attribution_required"])
        self.assertIn("Sam", by["openverse:aaa-1"]["attribution"])
        self.assertEqual(by["openverse:aaa-2"]["licence"]["name"], "Public Domain Mark 1.0")
        self.assertFalse(by["openverse:aaa-3"]["licence"]["commercial"])
        self.assertFalse(by["openverse:aaa-4"]["licence"]["derivatives"])
        self.assertIn("flickr", by["openverse:aaa-1"]["licence"]["note"])

    def test_openverse_url_licence_filter(self):
        q = urllib.parse.parse_qs(urllib.parse.urlsplit(FP.openverse_url("sea", 5, {"commercial": True,
                                                                                       "orientation": "portrait"})).query)
        self.assertEqual(q["license_type"], ["commercial,modification"])
        self.assertEqual(q["aspect_ratio"], ["tall"])

    def test_commons_images_only_ordered(self):
        rs = FP.parse_commons(COMMONS)
        self.assertEqual([r["id"] for r in rs], ["wikimedia:11", "wikimedia:13"])  # svg skipped, index order
        self.assertEqual(rs[0]["file_url"], "https://upload.wikimedia.org/s.jpg")  # utm stripped
        self.assertEqual(rs[0]["author"], "David Roberts")
        self.assertFalse(rs[0]["licence"]["attribution_required"])
        self.assertTrue(rs[1]["licence"]["share_alike"])
        self.assertIn("filetype:bitmap", FP.commons_url("x", 5, {}).replace("%3A", ":"))

    def test_nasa_largest_and_quoted(self):
        r = FP.parse_nasa(NASA)[0]
        self.assertEqual(r["id"], "nasa:iss 01")
        self.assertTrue(r["file_url"].startswith("https://") and "~orig" in r["file_url"] and " " not in r["file_url"])
        self.assertEqual((r["width"], r["height"]), (6048, 4032))
        self.assertIn("~medium", r["preview_url"])

    def test_met_public_domain_only(self):
        h, t = http({FP.MET_SEARCH: MET_SEARCH, **{FP.MET_OBJECT.format(id=k): v for k, v in MET_OBJ.items()}})
        rs = FP.search_met(h, "quran", 5, {})
        self.assertEqual([r["id"] for r in rs], ["met:1"])
        self.assertEqual(rs[0]["licence"]["name"], "CC0 1.0 (Met Open Access)")
        self.assertIn("9th c.", rs[0]["title"])
        self.assertIn("v1.1/search", t.seen[0][0])

    def test_pexels_pixabay_unsplash(self):
        p = FP.parse_pexels(PEXELS)[0]
        self.assertEqual((p["id"], p["sizes"]["large"]), ("pexels:77", "https://images.pexels.com/77-l.jpeg"))
        self.assertEqual(FP.orientation_of(p), "portrait")
        x = FP.parse_pixabay(PIXABAY)[0]
        self.assertEqual((x["width"], x["height"]), (1280, 853))  # largeImageURL is 1280 on the long side
        us = FP.parse_unsplash(UNSPLASH)
        self.assertEqual([u["id"] for u in us], ["unsplash:u1"])  # Unsplash+ skipped
        self.assertIn("utm_source=kosif", us[0]["page_url"])
        self.assertEqual(us[0]["download_location"], "https://api.unsplash.com/photos/u1/download")
        self.assertTrue(us[0]["attribution"].startswith("Photo by Omar on Unsplash"))


class SearchAndFilters(unittest.TestCase):
    def test_keys_gate_and_headers(self):
        h, t = http({FP.PEXELS_API: PEXELS, FP.UNSPLASH_API: UNSPLASH})
        rep = FP.run_search(h, "x", ["pexels", "unsplash", "pixabay"], 5, {}, environ={})
        self.assertEqual({s: v["status"] for s, v in rep["sources"].items()},
                         {"pexels": "skipped", "unsplash": "skipped", "pixabay": "skipped"})
        self.assertEqual(t.seen, [])  # no request without a key
        env = {"PEXELS_API_KEY": "pk-secret-123", "UNSPLASH_ACCESS_KEY": "us-secret-456"}
        rep = FP.run_search(h, "x", ["pexels", "unsplash"], 5, {}, environ=env)
        self.assertEqual(len(rep["results"]), 2)
        hdrs = {u.split("?")[0]: hd for u, hd in t.seen}
        self.assertEqual(hdrs[FP.PEXELS_API]["Authorization"], "pk-secret-123")
        self.assertEqual(hdrs[FP.UNSPLASH_API]["Authorization"], "Client-ID us-secret-456")
        self.assertNotIn("secret", json.dumps(rep))
        self.assertEqual(FP.default_sources({}), ["openverse", "wikimedia", "nasa", "met"])

    def test_filters(self):
        h, _ = http({FP.OPENVERSE_API: OPENVERSE})
        rep = FP.run_search(h, "x", ["openverse"], 10, {})
        self.assertEqual(rep["dropped"], {"nd-licence": 1})
        rep = FP.run_search(h, "x", ["openverse"], 10, {"commercial": True})
        self.assertEqual(sorted(r["id"] for r in rep["results"]), ["openverse:aaa-1", "openverse:aaa-2"])
        rep = FP.run_search(h, "x", ["openverse"], 10, {"orientation": "portrait"})
        self.assertEqual([r["id"] for r in rep["results"]], ["openverse:aaa-2"])
        rep = FP.run_search(h, "x", ["openverse"], 10, {"min_width": 3500})
        self.assertEqual([r["id"] for r in rep["results"]], ["openverse:aaa-1"])

    def test_one_failing_source_does_not_stop_others(self):
        h, _ = http({FP.NASA_SEARCH: NASA})
        rep = FP.run_search(h, "x", ["openverse", "nasa"], 5, {})
        self.assertEqual(rep["sources"]["openverse"]["status"], "error")
        self.assertEqual(rep["sources"]["nasa"]["status"], "ok")

    def test_merge_keeps_earlier_ids(self):
        a = FP.merge_results(None, {"query": "a", "searched_at": "t1", "sources": {}, "results": [{"id": "x:1"}]})
        b = FP.merge_results(a, {"query": "b", "searched_at": "t2", "sources": {}, "results": [{"id": "x:2"}, {"id": "x:1"}]})
        self.assertEqual([r["id"] for r in b["results"]], ["x:2", "x:1"])
        self.assertEqual([s["query"] for s in b["searches"]], ["b", "a"])


class DownloadAndCredits(unittest.TestCase):
    def test_download_sidecar_credits(self):
        rec = FP.parse_commons(COMMONS)[1]
        h, _ = http({"https://upload.wikimedia.org/g.jpg": JPG})
        with tempfile.TemporaryDirectory() as d:
            p = FP.download_one(h, rec, Path(d))
            self.assertEqual(p.name, "wikimedia-13.jpg")
            side = json.loads(FP.sidecar_for(p).read_text())
            self.assertEqual((side["schema"], side["bytes"]), (FP.ASSET_SCHEMA, len(JPG)))
            self.assertEqual(side["licence"]["name"], "CC BY-SA 4.0")
            md = FP.write_credits(Path(d)).read_text()
            self.assertIn("wikimedia-13.jpg", md)
            self.assertIn("Ahmed", md)
            self.assertIn("required", md)

    def test_refuses_web_page_and_nd(self):
        rec = FP.parse_commons(COMMONS)[1]
        h, _ = http({"https://upload.wikimedia.org/g.jpg": b"<!doctype html><title>blocked</title>"})
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(FP.PhotoError):
                FP.download_one(h, rec, Path(d))
            nd = [r for r in FP.parse_openverse(OPENVERSE) if r["id"] == "openverse:aaa-4"][0]
            with self.assertRaises(FP.PhotoError):
                FP.download_one(h, nd, Path(d))

    def test_unsplash_reports_download_first(self):
        rec = FP.parse_unsplash(UNSPLASH)[0]
        h, t = http({"https://api.unsplash.com/photos/u1/download": {"url": "x"},
                     "https://images.unsplash.com/p1": JPG})
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(FP.PhotoError):
                FP.download_one(h, rec, Path(d), environ={})
            FP.download_one(h, rec, Path(d), size="large", environ={"UNSPLASH_ACCESS_KEY": "us-secret-456"})
        self.assertEqual(t.seen[0][0], "https://api.unsplash.com/photos/u1/download")
        self.assertIn("w=2400", t.seen[1][0])

    def test_sheet_escapes(self):
        rec = FP.parse_openverse(OPENVERSE)[0]
        rec["title"] = '<script>"x"</script>'
        html = FP.sheet_html({"query": "q", "results": [rec]})
        self.assertNotIn("<script>", html)
        self.assertIn("openverse:aaa-1", html)

    def test_cli_sources_offline(self):
        out = io.StringIO()
        with mock.patch("sys.stdout", out):
            self.assertEqual(FP.main(["sources", "--json"]), 0)
        self.assertEqual(set(json.loads(out.getvalue())), set(FP.SOURCES))


if __name__ == "__main__":
    unittest.main()
