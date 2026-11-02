"""Site snapshot (goclone capabilities in the skill), offline: a local fixture server on 127.0.0.1 stands in for
the site, so nothing leaves the machine.

    python3 -m unittest discover -s .claude/skills/kosif-superpowers/evals -p 'test_site_snapshot.py' -v
"""
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK / "scripts"))
import site_snapshot as S  # noqa: E402


def run(*argv):
    err = io.StringIO()
    with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
        rc = S.main(list(argv))
    return rc, err.getvalue()


class SiteSnapshotTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.srv = S.fixture_server()
        cls.base = f"http://127.0.0.1:{cls.srv.server_address[1]}"
        cls.td = tempfile.TemporaryDirectory()
        cls.out = Path(cls.td.name) / "snap"
        cls.rc, _ = run("snapshot", cls.base + "/", "--rights", "own", "--rights-note", "test fixture",
                        "--allow-private", "--out", str(cls.out), "--pages", "2", "-q")

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()
        cls.srv.server_close()
        cls.td.cleanup()

    def test_goclone_layout_and_assets(self):
        self.assertEqual(self.rc, 0)
        for rel in ("index.html", "css/site.css", "css/base.css", "js/app.js", "imgs/logo.svg",
                    "imgs/logo-2x.png", "imgs/bg.png", "imgs/favicon.png", "fonts/it.woff2", "pages/about.html"):
            self.assertTrue((self.out / rel).exists(), rel)

    def test_links_rewritten_to_local_copy(self):
        html = (self.out / "index.html").read_text()
        self.assertIn('href="css/site.css"', html)
        self.assertIn('src="js/app.js"', html)
        self.assertIn("imgs/logo-2x.png 2x", html)
        self.assertIn("url('imgs/bg.png')", html)
        self.assertIn('href="pages/about.html"', html)
        self.assertIn("data:image/png;base64", html)  # data: URIs untouched
        css = (self.out / "css/site.css").read_text()
        self.assertIn("url('../fonts/it.woff2')", css)
        self.assertIn('"base.css"', css)
        about = (self.out / "pages/about.html").read_text()
        self.assertIn('href="../css/site.css"', about)
        self.assertIn('href="../index.html"', about)

    def test_manifest_hashes_match_files(self):
        import hashlib
        m = json.loads((self.out / "manifest.json").read_text())
        self.assertEqual(m["schema"], "kosif.site_snapshot.manifest.v1")
        for rec in m["files"]:
            data = (self.out / rec["path"]).read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(), rec["sha256"], rec["path"])

    def test_rights_record(self):
        r = json.loads((self.out / "RIGHTS.json").read_text())
        self.assertEqual(r["basis"], "own")
        self.assertEqual(r["note"], "test fixture")

    def test_design_readout(self):
        d = json.loads((self.out / "design.json").read_text())
        colors = [c for c, _ in d["colors"]]
        self.assertIn("#0a84ff", colors)
        self.assertIn("#ff5500", colors)
        self.assertEqual(d["font_families"][0][0], "Inter Tight")
        self.assertEqual(d["css_variables"]["--radius"], "14px")
        self.assertIn("768px", d["breakpoints"])
        self.assertIn("64px", [v for v, _ in d["font_sizes"]])
        self.assertIn("design.md", (self.out / "design.md").read_text())

    def test_refusals(self):
        o = str(Path(self.td.name) / "r")
        self.assertEqual(run("snapshot", self.base + "/", "--allow-private", "--out", o)[0], 1)  # no rights
        self.assertEqual(run("snapshot", self.base + "/", "--rights", "own", "--allow-private", "--out", o)[0], 1)
        self.assertEqual(run("snapshot", self.base + "/", "--rights", "own", "--rights-note", "x",
                             "--out", o)[0], 1)  # private address without --allow-private
        rc, err = run("snapshot", self.base + "/private", "--rights", "licensed", "--rights-note", "x",
                      "--allow-private", "--out", o)
        self.assertEqual(rc, 1)
        self.assertIn("robots.txt", err)
        self.assertEqual(run("snapshot", self.base + "/", "--rights", "licensed", "--rights-note", "x",
                             "--allow-private", "--ignore-robots", "--out", o)[0], 1)

    def test_size_cap(self):
        o = str(Path(self.td.name) / "cap")
        rc, err = run("snapshot", self.base + "/", "--rights", "own", "--rights-note", "x", "--allow-private",
                      "--out", o, "--max-file-mb", "0.0001")
        self.assertEqual(rc, 1)
        self.assertIn("size cap", err)

    def test_same_origin_assets_and_analyse(self):
        rc, _ = run("analyse", str(self.out), "--json")
        self.assertEqual(rc, 0)
        self.assertEqual(run("doctor", "--json")[0], 0)

    def test_goclone_engine_missing_is_refused(self):
        import unittest.mock as mock
        with mock.patch.object(S, "_goclone_bin", return_value=None):
            rc, err = run("snapshot", self.base + "/", "--engine", "goclone", "--rights", "own",
                          "--rights-note", "x", "--allow-private", "--out", str(Path(self.td.name) / "g"))
        self.assertEqual(rc, 1)
        self.assertIn("go install", err)

    def test_self_test(self):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(S.self_test(), 0)


if __name__ == "__main__":
    unittest.main()
