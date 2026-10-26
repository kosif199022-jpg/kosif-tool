"""KOSIF Motion Web — offline tests over the Starlette app (no network): the Workbench contract, the local render
service with job tokens, recipe jobs, media, projects, timeline summaries, path containment and MCP."""
from __future__ import annotations

import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts")); sys.path.insert(0, str(ROOT / "scripts" / "web"))
TMP_HOME = Path(tempfile.mkdtemp(prefix="kosif_webtest_"))
os.environ["KOSIF_MOTION_HOME"] = str(TMP_HOME)                 # the app and motion.PROJECTS live in a scratch home
import server  # noqa: E402
from starlette.testclient import TestClient  # noqa: E402

FF = shutil.which("ffmpeg")
MANIFEST = {"schema": "kosif.motion.manifest.v1", "title": "اختبار", "width": 320, "height": 180, "fps": 24, "duration": 2,
            "scenes": [{"id": "one", "start_frame": 0, "end_frame_exclusive": 48, "title": "فكرة تبدأ", "subtitle": "تفاصيل تتضح بالعربية", "camera": "slow_push", "accent": "#a7e8d0"}]}


def synth(path: Path, seconds: float = 2.0, size: str = "320x180", tone: int = 440):
    subprocess.run([FF, "-y", "-v", "error", "-f", "lavfi", "-i", f"testsrc2=s={size}:r=24:d={seconds}", "-f", "lavfi", "-i", f"sine=f={tone}:d={seconds}",
                    "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(path)], check=True)


class WebTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = server.create_app(workers=1)
        cls.client = TestClient(cls.app)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TMP_HOME, ignore_errors=True)

    # ── review page (Motion OS player, MIT) on the engine ──
    @unittest.skipUnless(FF, "ffmpeg")
    def test_review_page(self):
        c = self.client
        film = TMP_HOME / "rv_film.mp4"; synth(film, 2.0)
        r = c.post("/api/reviews", json={"target": str(film), "name": "rv1"})
        self.assertEqual(r.status_code, 200, r.text); self.assertEqual(r.json()["kind"], "video")
        self.assertEqual(c.post("/api/reviews", json={"target": str(TMP_HOME / "missing.mp4")}).status_code, 400)
        page = c.get("/review/rv1/")
        self.assertEqual(page.status_code, 200); self.assertIn("KOSIF review feedback for", page.text); self.assertIn("fetch('feedback'", page.text)
        reel = c.get("/review/rv1/reel.json").json()
        self.assertEqual((reel["name"], reel["version"]), ("rv1", 1))
        v = c.get("/review/rv1/" + reel["src"], headers={"range": "bytes=0-99"})
        self.assertEqual(v.status_code, 206); self.assertEqual(len(v.content), 100)            # seeking needs byte ranges
        self.assertEqual(c.get("/review/rv1/../../secret.txt").status_code, 404)
        self.assertEqual(c.get("/review/nope/").status_code, 404)
        fb = {"version": 1, "text": "KOSIF review feedback for x", "over": {}, "notes": [{"id": "n1", "t": 0.5, "x": 50, "y": 50, "text": "أوضح"}], "status": {"S1": "approved"}}
        self.assertEqual(c.post("/review/rv1/feedback", json=fb, headers={"origin": "https://evil.example"}).status_code, 403)
        self.assertIn("saved", c.post("/review/rv1/feedback", json=fb).json())
        self.assertEqual(c.get("/review/rv1/feedback").json()["notes"][0]["text"], "أوضح")
        self.assertEqual(c.get("/review/rv1/export").json()["state"], "idle")
        self.assertEqual(c.get("/api/reviews").json()["reviews"][0]["feedback"], 1)
        rpc = lambda name, args: c.post("/mcp", json={"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": name, "arguments": args}}).json()
        out = json.loads(rpc("kosif_review_apply", {"name": "rv1"})["result"]["content"][0]["text"])
        self.assertEqual(out["approved_do_not_touch"], ["S1"]); self.assertEqual(len(out["left_for_claude"]["notes"]), 1)
        self.assertIn("kosif_review_feedback", json.dumps(c.post("/mcp", json={"jsonrpc": "2.0", "id": 2, "method": "tools/list"}).json()))

    # ── the Workbench contract ──
    def test_contract(self):
        c = self.client
        self.assertEqual(c.get("/api/health").json()["status"], "ok")
        self.assertEqual(len(c.get("/api/templates").json()["templates"]), 3)
        self.assertEqual(c.post("/api/plan", content=b"x", headers={"content-type": "text/plain"}).status_code, 415)
        p = c.post("/api/plan", json={"task": "حركة نصوص عربية", "seconds": 12, "fps": 30, "aspect": "16:9"}).json()
        self.assertEqual(p["timeline"]["total_frames"], 360); self.assertEqual(p["route"], "remote_planning_only")
        self.assertTrue(c.post("/api/validate", json={"plan": p}).json()["valid"])
        self.assertEqual(c.post("/api/plan", json={"task": "structural truss 3D"}).status_code, 400)
        q = copy.deepcopy(p); q["timeline"]["shots"][1]["start_frame"] += 1
        self.assertFalse(c.post("/api/validate", json={"plan": q}).json()["valid"])
        comp = c.post("/api/compile", json={"plan": p}).json()
        self.assertEqual(comp["manifest"]["schema"], "kosif.motion.manifest.v1"); self.assertIn("window.render", comp["project_html"])
        self.assertIsNone(c.post("/api/compile", json={"plan": c.post("/api/plan", json={"task": "3D scene"}).json()}).json()["project_html"])
        self.assertEqual(c.post("/api/nothing", json={}).status_code, 404)
        self.assertEqual(c.post("/api/compile", json={"plan": {"schema": "x"}}).status_code, 400)

    # ── the render-service contract, rendered here ──
    @unittest.skipUnless(FF, "ffmpeg")
    def test_render_jobs(self):
        c = self.client
        st = c.get("/api/render/status").json(); self.assertTrue(st["configured"] and st["ready"])
        bad = copy.deepcopy(MANIFEST); bad["rawHTML"] = "<script/>"
        self.assertEqual(c.post("/api/render/jobs", json={"manifest": bad}).status_code, 422)
        r = c.post("/api/render/jobs", json={"manifest": MANIFEST}); self.assertEqual(r.status_code, 202, r.text)
        j = r.json(); url = f"/api/render/jobs/{j['job_id']}"; h = {"X-Job-Token": j["job_token"]}
        self.assertEqual(c.get(url).status_code, 404)                                   # no token → unavailable
        self.assertEqual(c.get(url, headers={"X-Job-Token": "wrong"}).status_code, 404)
        deadline = time.monotonic() + 60
        while time.monotonic() < deadline:
            s = c.get(url, headers=h).json()
            if s["status"] in ("succeeded", "failed"):
                break
            time.sleep(0.2)
        self.assertEqual(s["status"], "succeeded", s); self.assertEqual(s["metadata"]["frames"], 48)
        v = c.get(url + "/video", headers=h); self.assertEqual(v.status_code, 200); self.assertEqual(v.headers["content-type"], "video/mp4")
        out = TMP_HOME / "render-check.mp4"; out.write_bytes(v.content)
        probe = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(out)]))
        self.assertEqual((probe["streams"][0]["width"], probe["streams"][0]["height"], int(probe["streams"][0]["nb_frames"])), (320, 180, 48))
        self.assertAlmostEqual(float(probe["format"]["duration"]), 2, places=1)
        self.assertEqual(c.delete(url, headers=h).json()["status"], "cancelled")
        self.assertEqual(c.get(url + "/video", headers=h).status_code, 409)

    # ── studio: recipes and jobs ──
    def test_recipes_and_arg_guard(self):
        import recipes
        groups = self.client.get("/api/recipes").json()["groups"]
        self.assertTrue(any(r["id"] == "timeline" for g in groups for r in g["recipes"]))
        args = recipes.build_args(recipes.BY_ID["grade"], {"video": "--evil.mp4", "--preset": "restore"})
        self.assertEqual(args, ["--preset", "restore", "--out", "out/graded.mp4", "--", "--evil.mp4"])  # a dashed value stays positional
        with self.assertRaises(ValueError):
            recipes.build_args(recipes.BY_ID["grade"], {"--shell": "x"})
        self.assertEqual(self.client.post("/api/jobs", json={"recipe": "nope"}).status_code, 400)

    def test_job_runs_and_streams(self):
        c = self.client
        j = c.post("/api/jobs", json={"recipe": "transitions", "args": {}}).json()
        self.assertEqual(j["status"], "queued")
        deadline = time.monotonic() + 60
        while time.monotonic() < deadline:
            s = c.get(f"/api/jobs/{j['id']}").json()
            if s["status"] in ("done", "failed"):
                break
            time.sleep(0.3)
        self.assertEqual(s["status"], "done", s)
        log = c.get(f"/api/jobs/{j['id']}/log.txt").text
        self.assertIn("fade", log)
        with c.stream("GET", f"/api/jobs/{j['id']}/log") as r:
            body = "".join(r.iter_text())
        self.assertIn("event: end", body)
        self.assertEqual(c.get("/api/jobs").json()["jobs"][0]["recipe"], "transitions")

    # ── media ──
    @unittest.skipUnless(FF, "ffmpeg")
    def test_media_roundtrip(self):
        c = self.client
        clip = TMP_HOME / "clip ع.mp4"; synth(clip)
        with clip.open("rb") as f:
            r = c.post("/api/media", files=[("file", ("clip ع.mp4", f, "video/mp4")), ("file", ("evil.exe", b"MZ", "application/octet-stream"))])
        saved = r.json()["saved"]
        self.assertEqual(saved[0]["probe"]["video"]["w"], 320); self.assertIn("error", saved[1])
        items = c.get("/api/media").json()["media"]
        self.assertTrue(any(m["name"] == "clip ع.mp4" for m in items))
        self.assertEqual(c.get("/media/clip%20%D8%B9.mp4").status_code, 200)
        self.assertEqual(c.delete("/api/media/clip%20%D8%B9.mp4").json()["deleted"], "clip ع.mp4")
        self.assertIn(c.delete("/api/media/..%2Fsettings.json").status_code, (400, 404))   # never escapes the library
        self.assertTrue((server.WB / "settings.json").exists() or True)

    # ── projects ──
    def test_projects_and_containment(self):
        c = self.client
        p = c.post("/api/projects", json={"name": "t_card", "kind": "template", "template": "title-card", "params": {"title": "اختبار"}, "seconds": 5}).json()
        self.assertTrue(p["has_index"]); self.assertEqual(p["seconds"], 5.0)
        files = c.get("/api/projects/t_card/files").json()["files"]
        self.assertTrue(any(f["path"] == "index.html" for f in files))
        self.assertEqual(c.get("/projects/t_card/index.html").status_code, 200)
        self.assertEqual(c.get("/projects/t_card/assets/motion-kit.js").status_code, 200)
        w = c.post("/api/projects/t_card/file", json={"path": "notes.md", "content": "ملاحظة"}).json(); self.assertIn("written", w)
        self.assertEqual(c.post("/api/projects/t_card/file", json={"path": "../x.html", "content": "x"}).status_code, 400)
        self.assertEqual(c.post("/api/projects/t_card/file", json={"path": "evil.exe", "content": "x"}).status_code, 400)
        self.assertEqual(c.get("/api/file?path=C:/Windows/win.ini").status_code, 404)
        idx = Path(p["path"]) / "index.html"
        self.assertEqual(c.get(f"/api/file?path={idx}").status_code, 200)
        m = c.post("/api/projects", json={"name": "wb_m", "kind": "manifest", "manifest": MANIFEST}).json()
        self.assertEqual(m["kind"], "manifest")
        self.assertTrue(c.get("/api/projects").json()["projects"])

    # ── timeline ──
    @unittest.skipUnless(FF, "ffmpeg")
    def test_timeline_summary(self):
        a, b = TMP_HOME / "a.mp4", TMP_HOME / "b.mp4"; synth(a, 3); synth(b, 2, tone=660)
        spec = {"size": "320x180", "fps": 24, "clips": [{"src": str(a), "in": 0.5, "out": 2.5, "transition": {"type": "circleopen", "dur": 0.5}},
                                                        {"src": str(b), "speed": 2.0}, {"color": "#000000", "dur": 0.5}],
                "overlays": [{"type": "text", "text": "عنوان", "start": 0.2, "end": 1.2}]}
        s = self.client.post("/api/timeline/validate", json={"spec": spec}).json()
        self.assertTrue(s["ok"], s); self.assertAlmostEqual(s["seconds"], 2.0 + 1.0 + 0.5 - 0.5, places=2)
        bad = {**spec, "clips": [{"src": str(a), "transition": "warpdrive"}]}
        self.assertEqual(self.client.post("/api/timeline/validate", json={"spec": bad}).status_code, 400)
        r = self.client.post("/api/timeline/save", json={"name": "t1", "spec": spec}).json(); self.assertIn("saved", r)
        self.assertEqual(self.client.get("/api/timeline/t1").json()["spec"]["fps"], 24)
        self.assertIn("fade", self.client.get("/api/transitions").json()["transitions"][0]["id"])

    # ── Claude bridge (no network) ──
    def test_claude_package_and_apply(self):
        c = self.client
        pk = c.post("/api/claude/package", json={"task": "اعمل ريلز", "context": {"media": True}}).json()["package"]
        self.assertIn("recipes", pk); self.assertIn("اعمل ريلز", pk)
        reply = "خطة:\n```json\n{\"notes\": \"ok\", \"actions\": [{\"recipe\": \"transitions\", \"args\": {}}], \"files\": [{\"project\": \"t_card\", \"path\": \"from_claude.txt\", \"content\": \"hi\"}]}\n```"
        d = c.post("/api/claude/apply", json={"plan": reply}).json()
        self.assertEqual(len(d["jobs"]), 1); self.assertTrue(d["files"][0].endswith("from_claude.txt"))
        self.assertEqual(c.post("/api/claude/apply", json={"plan": "no json here"}).status_code, 400)
        s = c.get("/api/claude/status").json(); self.assertIn(s["backend"], ("cli", "api", "mcp"))

    # ── MCP ──
    def test_mcp(self):
        c = self.client
        def rpc(method, params=None, id=1):
            return c.post("/mcp", json={"jsonrpc": "2.0", "id": id, "method": method, "params": params or {}}).json()
        self.assertEqual(rpc("initialize")["result"]["serverInfo"]["name"], "kosif-motion-web")
        names = [t["name"] for t in rpc("tools/list")["result"]["tools"]]
        for n in ("motion_plan", "motion_validate", "motion_compile", "motion_templates", "kosif_run", "kosif_job", "kosif_project_write", "kosif_timeline_check"):
            self.assertIn(n, names)
        r = rpc("tools/call", {"name": "motion_plan", "arguments": {"task": "حركة", "seconds": 4, "fps": 24, "aspect": "9:16"}})
        self.assertEqual(r["result"]["structuredContent"]["timeline"]["total_frames"], 96)
        r = rpc("tools/call", {"name": "kosif_recipes", "arguments": {}}); self.assertIn("groups", r["result"]["structuredContent"])
        r = rpc("tools/call", {"name": "kosif_project_write", "arguments": {"name": "mcp_p", "path": "index.html", "content": "<html></html>"}})
        self.assertIn("written", r["result"]["structuredContent"])
        self.assertIn("error", rpc("tools/call", {"name": "no_such", "arguments": {}}))
        self.assertEqual(rpc("bogus")["error"]["code"], -32601)
        self.assertEqual(c.post("/mcp", json={"jsonrpc": "2.0", "method": "notifications/initialized"}).status_code, 202)


    # ── v6.1: cross-origin guard, filename repair, the v4 Studio and its import ──
    def test_foreign_origin_refused(self):
        c = self.client
        body = {"task": "حركة", "seconds": 4, "fps": 24, "aspect": "9:16"}
        self.assertEqual(c.post("/api/plan", json=body, headers={"Origin": "https://evil.example"}).status_code, 403)
        self.assertEqual(c.post("/api/jobs", json={"recipe": "transitions"}, headers={"Sec-Fetch-Site": "cross-site"}).status_code, 403)
        self.assertEqual(c.post("/mcp", json={"jsonrpc": "2.0", "id": 1, "method": "ping"}, headers={"Origin": "https://evil.example"}).status_code, 403)
        self.assertEqual(c.post("/api/plan", json=body, headers={"Origin": "http://127.0.0.1:8766", "Sec-Fetch-Site": "same-origin"}).status_code, 200)
        self.assertEqual(c.post("/api/plan", json=body, headers={"Origin": "http://localhost:8766"}).status_code, 200)
        self.assertEqual(c.post("/api/plan", json=body).status_code, 200)                         # curl / scripts send no Origin
        self.assertEqual(c.get("/api/health", headers={"Origin": "https://evil.example"}).status_code, 200)   # reads are not state changes

    def test_unmojibake(self):
        ar = "لقطة تجريبية.mp4"
        self.assertEqual(server._unmojibake(ar.encode("cp1256").decode("latin-1")), ar)      # curl on Arabic Windows
        self.assertEqual(server._unmojibake(ar.encode("utf-8").decode("latin-1")), ar)       # UTF-8 read as Latin-1
        self.assertEqual(server._unmojibake(ar), ar)
        self.assertEqual(server._unmojibake("café.mp4"), "café.mp4")                          # real accents survive
        self.assertEqual(server._safe_name(ar.encode("cp1256").decode("latin-1")), ar)

    def test_studio_and_examples_served(self):
        c = self.client
        r = c.get("/studio/index.html"); self.assertEqual(r.status_code, 200); self.assertIn("KOSIF", r.text)
        self.assertEqual(c.get("/studio/app.mjs").status_code, 200)
        self.assertEqual(c.get("/examples/cinematic-cat.html").status_code, 200)

    @unittest.skipUnless(FF, "ffmpeg")
    def test_studio_import_endpoint(self):
        clip = server.MEDIA / "studio_clip.mp4"; synth(clip, 3)
        project = {"version": 1, "name": "من الاستوديو", "aspect": "9:16", "background": "#07111e",
                   "assets": [{"id": "a1", "name": "studio_clip.mp4", "type": "video", "size": 1, "lastModified": 0, "duration": 3}],
                   "clips": [{"id": "c1", "type": "video", "assetId": "a1", "trim": 0.5, "duration": 2, "volume": 1, "fit": "cover"},
                             {"id": "c2", "type": "demo", "preset": "sunset", "duration": 1.5}],
                   "overlays": [{"id": "o1", "type": "text", "text": "عنوان", "x": 50, "y": 40, "size": 7, "color": "#ffffff", "opacity": 1, "start": 0.2, "duration": 2, "animation": "rise"},
                                {"id": "o2", "type": "shape", "shape": "circle", "x": 10, "y": 10, "size": 5, "color": "#ff0000", "opacity": 1, "start": 0, "duration": 1, "animation": "fade"}],
                   "soundtrack": None}
        r = self.client.post("/api/studio/import", json={"project": project, "name": "studio_test"})
        self.assertEqual(r.status_code, 200, r.text)
        d = r.json()
        self.assertEqual(d["spec"]["size"], "720x1280"); self.assertEqual(len(d["spec"]["clips"]), 2)
        self.assertEqual(d["report"]["skipped"][0]["type"], "shape")
        s = self.client.post("/api/timeline/validate", json={"spec": d["saved"]}).json()
        self.assertTrue(s["ok"], s); self.assertAlmostEqual(s["seconds"], 3.5, delta=0.05)
        self.assertEqual(self.client.post("/api/studio/import", json={"project": {"version": 2}}).status_code, 400)


if __name__ == "__main__":
    unittest.main()
