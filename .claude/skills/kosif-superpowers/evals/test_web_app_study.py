"""web_app_study.py: guardrails, facts-only report, and (when REA + Chromium exist) a live study of a local page."""
import http.server
import json
import socket
import sys
import tempfile
import threading
import unittest
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK / "scripts"))
import web_app_study as W  # noqa: E402


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def fake_study(root: Path):
    """A synthetic study folder shaped like REA's outputs (no third-party code)."""
    files = root / "scripts-export" / "files" / "isolated"
    files.mkdir(parents=True)
    (files / "source-1-aaaa.js").write_text(
        'var a={version:"19.1.0",rendererPackageName:"react-dom"};var b="@tldraw/editor";self.__next_f=[];', encoding="utf-8")
    (files / "source-2-bbbb.js").write_text('var c="https://x.firebaseapp.com";var d="y-protocols";var e="--tw-ring-color";var f=("firebase","11.10.0","app");', encoding="utf-8")
    cap = {"normalized_result": {
        "target": {"url": "https://app.example/", "title": "Example App"},
        "capture_window": {"started_at": "2026-10-20T00:00:00Z"},
        "resources": [{"url": "https://app.example/_next/static/chunks/1.js?dpl=dpl_X", "type": "Script"},
                      {"url": "https://app.example/font.woff2", "type": "Font"}],
        "scripts": {"items": []}, "dom": {"total_nodes": 42}, "network": {"requests": [], "websocket_connections": []},
        "storage": {"local_storage_keys": ["_gcl_ls", "theme"], "session_storage_keys": ["mp_tab_id_mixpanel_123"],
                    "indexed_db_names": ["firebase-installations-database"]}}}
    (root / "02-page-capture.json").write_text(json.dumps(cap), encoding="utf-8")
    (root / "04-webmcp.json").write_text(json.dumps({"normalized_result": {"status": "available", "tools": {"items": [{"name": "search_designs"}]}}}),
                                         encoding="utf-8")


class Guardrails(unittest.TestCase):
    def test_origins_and_urls(self):
        self.assertEqual(W.origin_of("https://www.magicpath.ai/documentation?x=1"), "https://www.magicpath.ai")
        self.assertEqual(W.origin_of("http://127.0.0.1:8123/a"), "http://127.0.0.1:8123")
        for bad in ("file:///etc/passwd", "javascript:alert(1)", "chrome://settings", "https:///nohost"):
            with self.assertRaises(ValueError, msg=bad):
                W.origin_of(bad)

    def test_study_folder_must_be_outside_git_and_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "checkout"
            (repo / ".git").mkdir(parents=True)
            with self.assertRaisesRegex(ValueError, "outside any git checkout"):
                W.run("https://example.com", str(repo / "study"), dry_run=True)
            busy = Path(tmp) / "busy"; busy.mkdir(); (busy / "x").write_text("x")
            with self.assertRaisesRegex(ValueError, "new or empty"):
                W.run("https://example.com", str(busy), dry_run=True)
        # this very repository; a packaged copy of the skill (zip, package_skill output) has no checkout to refuse
        if W.inside_git(SK):
            with self.assertRaisesRegex(ValueError, "outside any git checkout"):
                W.run("https://example.com", str(SK / "tmp-study"), dry_run=True)

    def test_dry_run_plan_is_isolated_and_logged_out(self):
        with tempfile.TemporaryDirectory() as tmp:
            res = W.run("https://app.example/x", str(Path(tmp) / "s"), allow=["https://cdn.example"], dry_run=True, proxy="none")
            plan = res["plan"]
            self.assertEqual(plan["origins"], ["https://app.example", "https://cdn.example"])
            self.assertEqual(plan["login"], "never")
            argv = " ".join(plan["browser"])
            self.assertIn("--headless=new", argv)
            self.assertIn("--disable-background-networking", argv)            # only the studied site is contacted
            self.assertIn("--remote-debugging-address=127.0.0.1", argv)
            self.assertIn("--remote-debugging-port=0", argv)                  # the browser picks its port; verified by its profile
            self.assertIn("--disk-cache-dir=", argv)
            self.assertIn("--disable-crash-reporter", argv)
            self.assertIn(f"--user-data-dir={Path(tmp).resolve() / 's' / 'isolated-profile'}", argv)
            self.assertNotIn("--proxy-server", argv)
            self.assertFalse((Path(tmp) / "s").exists())                      # a dry run touches nothing
            steps = [s[0] for s in plan["rea_steps"]]
            self.assertEqual(steps, ["list-browser-targets", "inspect-web-page", "discover-webmcp-tools", "capture-web-screenshot", "export-web-scripts"])
            self.assertIn("--include-storage-keys", plan["rea_steps"][1])      # key names, never values
            self.assertNotIn("--include-console-text", plan["rea_steps"][1])
            deep = W.run("https://app.example", str(Path(tmp) / "d"), deep=True, dry_run=True)["plan"]["rea_steps"]
            self.assertEqual(deep[-1][0], "analyze-javascript-application")
            self.assertIn("--max-heap-mb", deep[-1])                           # bounded: the unbounded bundle analyzer ran out of memory


class NeverAttachToAnotherBrowser(unittest.TestCase):
    def _fake_devtools(self, ws_path):
        class H(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                body = json.dumps({"webSocketDebuggerUrl": f"ws://127.0.0.1/devtools/browser/{ws_path}"}).encode()
                self.send_response(200); self.end_headers(); self.wfile.write(body)

            def log_message(self, *a):
                pass
        srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        return srv

    def test_only_the_browser_this_run_started(self):
        class Alive:
            def poll(self):
                return None
        srv = self._fake_devtools("someone-elses-browser")
        try:
            with tempfile.TemporaryDirectory() as tmp:
                prof = Path(tmp)
                (prof / "DevToolsActivePort").write_text(f"{srv.server_port}\n/devtools/browser/our-browser\n")
                with self.assertRaisesRegex(RuntimeError, "another browser"):
                    W._wait_for_devtools(Alive(), prof, timeout=5)
                (prof / "DevToolsActivePort").write_text(f"{srv.server_port}\n/devtools/browser/someone-elses-browser\n")
                self.assertEqual(W._wait_for_devtools(Alive(), prof, timeout=5), f"http://127.0.0.1:{srv.server_port}")
        finally:
            srv.shutdown(); srv.server_close()
        with tempfile.TemporaryDirectory() as tmp, self.assertRaisesRegex(ValueError, "not used any more"):
            W.run("https://example.com", str(Path(tmp) / "s"), port=9223)

    def test_urls_proxies_and_logins(self):
        with self.assertRaisesRegex(ValueError, "login"):
            W.origin_of("https://user:secret@app.example/")
        self.assertEqual(W.origin_of("http://[::1]:8080/x"), "http://[::1]:8080")
        self.assertEqual(W.origin_of("https://bücher.example/"), "https://xn--bcher-kva.example")
        self.assertEqual(W.safe_url("https://app.example/p?token=abc&x=1#frag"), "https://app.example/p?token=…&x=…")
        with self.assertRaisesRegex(ValueError, "credentials"):
            W.proxy_arg("http://u:p@proxy.local:3128")
        import os
        old = os.environ.get("NO_PROXY")
        os.environ["NO_PROXY"] = "localhost,127.0.0.1"
        try:
            self.assertEqual(W.proxy_arg("http://127.0.0.1:3128"), ["--proxy-server=http://127.0.0.1:3128", "--proxy-bypass-list=localhost;127.0.0.1"])
        finally:
            os.environ.pop("NO_PROXY") if old is None else os.environ.__setitem__("NO_PROXY", old)


class Report(unittest.TestCase):
    def test_unchecked_webmcp_is_unknown_and_key_ids_are_masked(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake_study(root)
            (root / "04-webmcp.json").write_text(json.dumps({"normalized_result": {"status": "unavailable", "tools": {"items": []}}}), encoding="utf-8")
            cap = json.loads((root / "02-page-capture.json").read_text(encoding="utf-8"))
            cap["normalized_result"]["storage"]["local_storage_keys"].append("__mpq_a4ccb0cbf30074a8c35fc8ee722f5d86_ev")
            (root / "02-page-capture.json").write_text(json.dumps(cap), encoding="utf-8")
            rep = W.report(root)
            self.assertFalse(rep["webmcp"]["checked"])
            md = (root / "report.md").read_text(encoding="utf-8")
            self.assertIn("not checked (unavailable)", md)
            self.assertNotIn("none declared", md)
            self.assertNotIn("a4ccb0cbf30074a8c35fc8ee722f5d86", md + (root / "report.json").read_text(encoding="utf-8"))

    def test_failed_steps_are_unknown_and_odd_files_do_not_crash(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake_study(root)
            (root / "07-js-graph.json").write_text("[1, 2, 3]", encoding="utf-8")            # valid JSON, not an object
            (root / "receipts.json").write_text(json.dumps({"complete": False, "steps": [{"command": "discover-webmcp-tools", "rc": 1, "code": "provider_unavailable"}],
                                                            "artifacts": [{"file": "x.json"}]}), encoding="utf-8")
            cap = json.loads((root / "02-page-capture.json").read_text(encoding="utf-8"))
            cap["normalized_result"]["target"]["title"] = "Evil | title\n`with` breakers" + "x" * 300
            cap["normalized_result"]["resources"].append(None)
            (root / "02-page-capture.json").write_text(json.dumps(cap), encoding="utf-8")
            rep = W.report(root)
            self.assertIn("step failed: provider_unavailable", rep["webmcp"]["status"])
            self.assertNotIn("|", rep["title"]); self.assertNotIn("\n", rep["title"]); self.assertLessEqual(len(rep["title"]), 121)
            md = (root / "report.md").read_text(encoding="utf-8")
            self.assertIn("Incomplete study", md)
        with self.assertRaisesRegex(ValueError, "no study folder"):
            W.report("/nonexistent/study")

    def test_lookalike_names_are_not_libraries(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake_study(root)
            f = root / "scripts-export" / "files" / "isolated" / "source-3-cccc.js"
            f.write_text('throw Error(`linkifyjs: bad`);if("excalidraw/clipboard"===t){};var z={major:4,minor:1,patch:11};var y="$ZodType";', encoding="utf-8")
            names = {s["name"]: s for s in W.report(root)["stack"]}
            self.assertNotIn("Excalidraw", names)                  # a paste MIME type is not the engine
            self.assertEqual(names["Zod"]["version"], "4.1.11")
            self.assertEqual(names["Yjs"]["files"], 1)              # only the real y-protocols file, not linkifyjs

    def test_facts_only_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake_study(root)
            rep = W.report(root)
            names = {s["name"]: s for s in rep["stack"]}
            for n in ("Next.js", "Vercel", "React", "tldraw", "Firebase SDK", "Yjs", "Tailwind CSS"):
                self.assertIn(n, names, n)
            self.assertEqual(names["React"]["version"], "19.1.0")
            self.assertEqual(names["Firebase SDK"]["version"], "11.10.0")
            self.assertEqual({x["service"] for x in rep["services_from_storage_key_names"]}, {"Google Ads", "Mixpanel", "Firebase"})
            self.assertIn("theme", rep["unclassified_storage_keys"])
            self.assertEqual(rep["webmcp"]["tools"], ["search_designs"])
            self.assertEqual(rep["page"]["scripts_exported"], 2)
            md = (root / "report.md").read_text(encoding="utf-8")
            self.assertIn("| framework | React | 19.1.0 | observed |", md)
            for code in ("rendererPackageName:\"react-dom\"", "var a=", "self.__next_f=[]"):  # never code
                self.assertNotIn(code, md)
                self.assertNotIn(code, (root / "report.json").read_text(encoding="utf-8"))


@unittest.skipUnless(W.find_rea() and W.find_chromium(), "needs REA and a Chromium browser")
class LiveLocalPage(unittest.TestCase):
    def test_study_a_local_page_end_to_end(self):
        with tempfile.TemporaryDirectory() as site, tempfile.TemporaryDirectory() as tmp:
            Path(site, "index.html").write_text('<!doctype html><title>Local Study</title><script src="app.js"></script><p>hi</p>', encoding="utf-8")
            Path(site, "app.js").write_text('localStorage.setItem("_gcl_ls","1");window.__next_f=[];document.title="Local Study";', encoding="utf-8")
            handler = lambda *a, **k: http.server.SimpleHTTPRequestHandler(*a, directory=site, **k)  # noqa: E731
            http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
            srv = http.server.ThreadingHTTPServer(("127.0.0.1", free_port()), handler)
            threading.Thread(target=srv.serve_forever, daemon=True).start()
            try:
                out = Path(tmp) / "study"
                res = W.run(f"http://127.0.0.1:{srv.server_port}/", str(out), obs_ms=800, proxy="none", settle_s=2.0)
            finally:
                srv.shutdown()
                srv.server_close()
            self.assertTrue(all(s["rc"] == 0 for s in res["steps"]), res["steps"])
            self.assertTrue(res["complete"])
            self.assertTrue(res["profile_deleted"])
            rec = json.loads((out / "receipts.json").read_text(encoding="utf-8"))
            self.assertTrue(rec["profile_deleted"])
            self.assertTrue(rec["browser"].startswith(("Chrome/", "HeadlessChrome/")), rec["browser"])
            self.assertFalse((out / "isolated-profile").exists())             # no cookies or cache survive
            self.assertTrue((out / "screenshot.png").exists())
            self.assertTrue(all(len(a["sha256"]) == 64 for a in rec["artifacts"]))
            rep = json.loads((out / "report.json").read_text(encoding="utf-8"))
            self.assertEqual(rep["title"], "Local Study")
            self.assertIn("Google Ads", [x["service"] for x in rep["services_from_storage_key_names"]])


if __name__ == "__main__":
    unittest.main(verbosity=2)
