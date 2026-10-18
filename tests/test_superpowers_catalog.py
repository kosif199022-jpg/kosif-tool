"""Checks for the tool catalog, doctor, reference fetcher and font-matching parts of .claude/skills/kosif-superpowers (stdlib only).

The skill's power catalog and proofs are covered by tests/test_superpowers.py; this module covers repos.json,
references/capabilities.md, scripts/superpowers.py, scripts/fetch_reference.py and scripts/render_text.cjs."""
from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _fixture import REAL_ROOT  # noqa: E402

SKILL = REAL_ROOT / ".claude" / "skills" / "kosif-superpowers"
SCRIPTS = SKILL / "scripts"
PY = sys.executable
ARABIC = re.compile(r"[؀-ۿ]")
LINK = re.compile(r"\]\((?!https?://|#|mailto:)([^)\s]+)\)")
SKILL_FILES = (
    "SKILL.md",
    "repos.json",
    "references/capabilities.md",
    "references/repos.md",
    "references/reference-inspection.md",
    "references/font-matching.md",
    "scripts/superpowers.py",
    "scripts/fetch_reference.py",
    "scripts/render_text.cjs",
)


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_script(script: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([PY, str(SCRIPTS / script), *args], capture_output=True, text=True, cwd=REAL_ROOT)


class SkillFilesTest(unittest.TestCase):
    def setUp(self):
        self.skill_md = (SKILL / "SKILL.md").read_text(encoding="utf-8")

    def test_all_files_present(self):
        for rel in SKILL_FILES:
            with self.subTest(file=rel):
                self.assertTrue((SKILL / rel).exists(), rel)

    def test_frontmatter(self):
        m = re.match(r"^---\n(.*?)\n---\n", self.skill_md, re.S)
        self.assertIsNotNone(m, "SKILL.md must start with YAML frontmatter")
        self.assertRegex(m.group(1), r"(?m)^name: kosif-superpowers$")

    def test_skill_md_routes_to_the_catalog_files(self):
        for needle in ("repos.json", "references/repos.md", "references/capabilities.md", "references/reference-inspection.md", "references/font-matching.md", "scripts/fetch_reference.py", "scripts/superpowers.py", "scripts/render_text.cjs"):
            with self.subTest(file=needle):
                self.assertIn(needle, self.skill_md)

    def test_capabilities_md_names_every_capability_key(self):
        data = json.loads((SKILL / "repos.json").read_text(encoding="utf-8"))
        text = (SKILL / "references" / "capabilities.md").read_text(encoding="utf-8")
        for cap in data["capabilities"]:
            with self.subTest(capability=cap):
                self.assertRegex(text, rf"(?m)^## {cap}\b")

    OWN_DOCS = ("references/capabilities.md", "references/repos.md", "references/reference-inspection.md", "references/font-matching.md")

    def test_markdown_is_bilingual_and_links_resolve(self):
        for md in [SKILL / rel for rel in self.OWN_DOCS]:
            text = md.read_text(encoding="utf-8")
            with self.subTest(file=md.name):
                self.assertTrue(ARABIC.search(text), "Arabic text expected")
                self.assertRegex(text, r"[A-Za-z]{4,}", "English text expected")
                for link in LINK.findall(text):
                    target = (md.parent / link.split("#", 1)[0]).resolve()
                    self.assertTrue(target.exists(), f"{md.name}: broken link {link}")

    def test_capabilities_md_has_a_section_per_used_capability(self):
        data = json.loads((SKILL / "repos.json").read_text(encoding="utf-8"))
        text = (SKILL / "references" / "capabilities.md").read_text(encoding="utf-8")
        used = {r["capability"] for r in data["repos"]}
        for cap in used:
            with self.subTest(capability=cap):
                self.assertRegex(text, rf"(?m)^## {cap}\b")


class CatalogTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sp = load_module("kosif_superpowers_cli", SCRIPTS / "superpowers.py")
        cls.data = json.loads((SKILL / "repos.json").read_text(encoding="utf-8"))

    def test_validator_finds_no_problems(self):
        self.assertEqual(self.sp.validate(self.data, REAL_ROOT), [])

    def test_exactly_124_unique_github_repositories(self):
        repos = self.data["repos"]
        self.assertEqual(len(repos), 124)
        keys = {r["owner_repo"].lower() for r in repos}
        self.assertEqual(len(keys), 124)
        for r in repos:
            self.assertEqual(r["url"], f"https://github.com/{r['owner_repo']}")

    def test_every_capability_has_repositories_and_quotas_hold(self):
        counts = {}
        for r in self.data["repos"]:
            counts[r["capability"]] = counts.get(r["capability"], 0) + 1
        for cap in self.data["capabilities"]:
            with self.subTest(capability=cap):
                self.assertGreaterEqual(counts.get(cap, 0), 3, f"{cap} needs at least three repositories")
        self.assertGreaterEqual(len(self.data["domains"]), 10)

    def test_records_are_bilingual_and_credit_licenses(self):
        for r in self.data["repos"]:
            with self.subTest(repo=r["owner_repo"]):
                self.assertTrue(ARABIC.search(r["summary_ar"]))
                self.assertTrue(ARABIC.search(r["kosif_use_ar"]))
                self.assertFalse(ARABIC.search(r["summary_en"]))
                self.assertNotEqual(r["license"].strip().lower(), "")
                self.assertIn(r["license_note"], self.sp.LICENSE_NOTES)
                self.assertLessEqual(len(r["integration_en"]), 220)

    def test_playbooks_are_covered(self):
        referenced = {p for r in self.data["repos"] for p in r["playbooks"]}
        self.assertGreaterEqual(len(referenced), 10, f"only {sorted(referenced)} referenced")
        for p in referenced:
            self.assertTrue((REAL_ROOT / p).exists(), p)

    def test_repos_md_is_generated_from_repos_json(self):
        proc = run_script("superpowers.py", "check")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        text = (SKILL / "references" / "repos.md").read_text(encoding="utf-8")
        for r in self.data["repos"]:
            self.assertIn(r["url"], text)
        self.assertIn("Generated from `repos.json`", text)


class CliTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((SKILL / "repos.json").read_text(encoding="utf-8"))

    def test_list_json_returns_all(self):
        proc = run_script("superpowers.py", "list", "--json")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(len(json.loads(proc.stdout)), 124)

    def test_list_filters_by_capability(self):
        proc = run_script("superpowers.py", "list", "--capability", "voice", "--json")
        rows = json.loads(proc.stdout)
        self.assertTrue(rows)
        self.assertTrue(all(r["capability"] == "voice" for r in rows))

    def test_search_finds_a_known_name_and_rejects_nonsense(self):
        first = self.data["repos"][0]
        proc = run_script("superpowers.py", "search", first["owner_repo"].split("/")[1], "--json")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn(first["owner_repo"], [r["owner_repo"] for r in json.loads(proc.stdout)])
        proc = run_script("superpowers.py", "search", "zzqqxx-not-a-tool")
        self.assertEqual(proc.returncode, 1)

    def test_show_known_and_unknown(self):
        first = self.data["repos"][0]
        proc = run_script("superpowers.py", "show", first["owner_repo"])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn(first["url"], proc.stdout)
        self.assertTrue(ARABIC.search(proc.stdout))
        proc = run_script("superpowers.py", "show", "nobody/nothing")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("not in the catalog", proc.stderr)

    def test_doctor_json_shape(self):
        proc = run_script("superpowers.py", "doctor", "--json")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        rows = json.loads(proc.stdout)
        ids = {r["id"] for r in rows}
        for needed in ("node", "ffmpeg", "ffprobe", "playwright", "whisper", "gpu"):
            self.assertIn(needed, ids)
        for r in rows:
            self.assertIn("installed", r)
            self.assertIsInstance(r["installed"], bool)

    def test_stats_and_help_run(self):
        self.assertEqual(run_script("superpowers.py", "stats").returncode, 0)
        proc = run_script("superpowers.py")
        self.assertEqual(proc.returncode, 0)
        self.assertIn("doctor", proc.stdout)


class FetchReferenceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fr = load_module("kosif_fetch_reference", SCRIPTS / "fetch_reference.py")

    def test_find_media_urls_orders_direct_then_hls_then_untyped(self):
        page = """
        <html><head>
        <meta property="og:video:secure_url" content="https://cdn.example.com/v/clip.mp4?x=1">
        <meta name="twitter:player:stream" content="/stream/master.m3u8">
        <script type="application/ld+json">{"contentUrl":"https:\\/\\/cdn.example.com\\/ld\\/movie.webm"}</script>
        </head><body>
        <video src="blob:https://example.com/abc"><source src="player/source.mov" type="video/quicktime"></video>
        <video data-src="https://cdn.example.com/untyped/play"></video>
        <script>var u = "https://cdn.example.com/js/hidden.mp4";</script>
        </body></html>"""
        found = self.fr.find_media_urls(page, "https://example.com/page/")
        self.assertEqual(found[0], "https://cdn.example.com/v/clip.mp4?x=1")
        self.assertIn("https://cdn.example.com/ld/movie.webm", found)
        self.assertIn("https://example.com/page/player/source.mov", found)
        self.assertIn("https://cdn.example.com/js/hidden.mp4", found)
        self.assertIn("https://example.com/stream/master.m3u8", found)
        self.assertEqual(found[-1], "https://cdn.example.com/untyped/play")
        self.assertFalse(any(u.startswith("blob:") for u in found))
        direct = [u for u in found if self.fr.classify(u) == "direct"]
        hls = [u for u in found if self.fr.classify(u) == "hls"]
        self.assertLess(found.index(direct[-1]), found.index(hls[0]))

    def test_parse_master_and_pick_highest_bandwidth(self):
        master = "\n".join([
            "#EXTM3U",
            '#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="aud",NAME="ar",DEFAULT=YES,URI="audio/ar.m3u8"',
            '#EXT-X-STREAM-INF:BANDWIDTH=800000,RESOLUTION=640x360,AUDIO="aud"',
            "low/index.m3u8",
            "",
            '#EXT-X-STREAM-INF:BANDWIDTH=2400000,RESOLUTION=1080x1920,AUDIO="aud"',
            "high/index.m3u8",
        ])
        variants, audio = self.fr.parse_master(master, "https://cdn.example.com/hls/master.m3u8")
        self.assertEqual(len(variants), 2)
        best = self.fr.pick_variant(variants)
        self.assertEqual(best["url"], "https://cdn.example.com/hls/high/index.m3u8")
        self.assertEqual(best["resolution"], "1080x1920")
        self.assertEqual(audio["aud"], "https://cdn.example.com/hls/audio/ar.m3u8")

    def test_parse_media_detects_encryption_and_init_segment(self):
        base = "https://cdn.example.com/hls/high/index.m3u8"
        plain = "#EXTM3U\n#EXT-X-TARGETDURATION:4\n#EXT-X-MAP:URI=\"init.mp4\"\n#EXTINF:4.0,\nseg0.m4s\n#EXTINF:4.0,\nseg1.m4s\n#EXT-X-ENDLIST\n"
        media = self.fr.parse_media(plain, base)
        self.assertFalse(media["encrypted"])
        self.assertEqual(media["init"], "https://cdn.example.com/hls/high/init.mp4")
        self.assertEqual(media["segments"], ["https://cdn.example.com/hls/high/seg0.m4s", "https://cdn.example.com/hls/high/seg1.m4s"])
        self.assertEqual(media["target_duration"], 4.0)
        locked = plain.replace("#EXT-X-MAP", '#EXT-X-KEY:METHOD=AES-128,URI="k"\n#EXT-X-MAP')
        self.assertTrue(self.fr.parse_media(locked, base)["encrypted"])
        unlocked = plain.replace("#EXT-X-MAP", "#EXT-X-KEY:METHOD=NONE\n#EXT-X-MAP")
        self.assertFalse(self.fr.parse_media(unlocked, base)["encrypted"])

    def test_classify_slug_and_aspect(self):
        self.assertEqual(self.fr.classify("https://a.b/c/d.M3U8?token=1"), "hls")
        self.assertEqual(self.fr.classify("https://a.b/c/d.mp4"), "direct")
        self.assertEqual(self.fr.classify("https://a.b/watch?v=1"), "unknown")
        self.assertEqual(self.fr.slug_for("https://www.example.com/videos/My Clip.mp4"), "www.example.com-My-Clip-mp4")
        self.assertEqual(self.fr.aspect_label(1080, 1920), "9:16")
        self.assertEqual(self.fr.aspect_label(1920, 1080), "16:9")
        self.assertEqual(self.fr.aspect_label(1000, 1000), "1:1")
        self.assertEqual(self.fr.aspect_label(700, 320), "700:320")

    def test_cli_refuses_blob_urls_and_prints_help(self):
        proc = run_script("fetch_reference.py", "blob:https://example.com/x")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("blob:", proc.stderr)
        proc = run_script("fetch_reference.py", "--help")
        self.assertEqual(proc.returncode, 0)
        self.assertIn("--max-mb", proc.stdout)


class RepoWiringTest(unittest.TestCase):
    def test_entry_documents_point_to_the_skill(self):
        for name in ("CLAUDE.md", "AGENTS.md", "README.md"):
            with self.subTest(file=name):
                self.assertIn(".claude/skills/kosif-superpowers", (REAL_ROOT / name).read_text(encoding="utf-8"))

    def test_cache_directory_is_ignored(self):
        self.assertIn(".kosif-cache/", (REAL_ROOT / ".gitignore").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
